"""API."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.models import Confession
from src.schemas import ConfessionMessage, SupportedWSEvent, WSMessage

app = FastAPI()

template_path = Path(__file__).parent / "templates"

templates = Jinja2Templates(directory=template_path)


class ConnectionManager:
    """Websocket Manager."""

    def __init__(self) -> None:
        """Inialize."""
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket, user_id: str) -> None:
        """Connect Websocket."""
        await websocket.accept()
        websocket.user_id = user_id
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """Disconnect."""
        self.active_connections.remove(websocket)

    async def broadcast_json(self, message: dict) -> None:
        """Broadcast JSON."""
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

    @staticmethod
    def generate_user_id(headers: dict) -> str:
        """Renerate random User Id."""
        if headers.get("sec-websocket-key"):
            return hashlib.sha224(
                str(headers["sec-websocket-key"]).encode(),
            ).hexdigest()[:11]
        raw = (
            headers.get("user-agent", "")
            + headers.get("x-forwarded-for", "")
            + str(datetime.now(tz=timezone.utc).timestamp())
        )
        return hashlib.sha256(raw.encode()).hexdigest()[:8]


manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Index page."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.websocket("/ws/confessions")
async def websocket_endpoint(
    websocket: WebSocket,
) -> None:
    headers = dict(websocket.headers)
    user_id = manager.generate_user_id(headers)
    await manager.connect(websocket, user_id)

    try:
        while True:
            message = await websocket.receive_json()
            message = WSMessage(**message)
            match message.type:
                case SupportedWSEvent.CONFESSION.value:
                    confession = ConfessionMessage(text=message.details.text)

                    Confession.create_confession(message=confession)
                    message = confession.model_dump()
                    if "id" in message:
                        message["id"] = str(message["id"])
                    message["user_id"] = user_id

                    await manager.broadcast_json(
                        {
                            "type": SupportedWSEvent.CONFESSION.value,
                            "confession": message,
                        },
                    )
                case SupportedWSEvent.UPVOTE.value:
                    Confession.upvote_confession(
                        confession_id=message.details.confession_id,
                    )

                    await manager.broadcast_json(
                        {
                            "type": message.type,
                            "confession_id": str(message.details.confession_id),
                        },
                    )
                case SupportedWSEvent.COMMENT.value:
                    await manager.broadcast_json(
                        {
                            "type": message.type,
                            "confession_id": str(message.details.confession_id),
                            "comment": {
                                "user_id": user_id,
                                "text": message.details.text,
                                "timestamp": message.details.timestamp,
                            },
                        },
                    )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
