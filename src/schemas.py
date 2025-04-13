"""Data Schemas."""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, model_validator


class SupportedWSEvent(str, Enum):
    """WS Events."""

    CONFESSION = "confession"
    UPVOTE = "upvote"
    COMMENT = "comment"


class UpvoteMessage(BaseModel):
    """UpVote Message."""

    confession_id: Union[str, UUID]

    @field_validator("confession_id", mode="before")
    @classmethod
    def convert_to_uuid(cls, value) -> UUID:
        """Check if its UUID."""
        return value if isinstance(value, UUID) else UUID(value)


class ConfessionMessage(BaseModel):
    """Confenssion Message."""

    text: str
    id: Optional[UUID] = Field(  # noqa: FA100
        default_factory=lambda: uuid4(),
    )


class CommentMessage(BaseModel):
    """Confession Comment."""

    confession_id: Union[str, UUID]
    text: str

    @field_validator("confession_id", mode="before")
    @classmethod
    def convert_to_uuid(cls, value) -> UUID:
        """Check if its UUID."""
        return value if isinstance(value, UUID) else UUID(value)

    @property
    def timestamp(self) -> float:
        """Received timestamp."""
        return datetime.now(tz=timezone.utc).timestamp()


class WSMessage(BaseModel):
    """WS Message."""

    type: SupportedWSEvent
    details: Union[UpvoteMessage, ConfessionMessage, CommentMessage]

    @model_validator(mode="before")
    def pre_validation(self):
        """Pre pydantic validation. Self here is a dict of values."""
        if isinstance(self, dict):
            match self["type"]:
                case SupportedWSEvent.UPVOTE.value:
                    self["details"] = UpvoteMessage(**self["details"]).model_dump()
                case SupportedWSEvent.CONFESSION.value:
                    self["details"] = ConfessionMessage(**self["details"]).model_dump()
                case SupportedWSEvent.COMMENT.value:
                    self["details"] = CommentMessage(**self["details"]).model_dump()
                case _:
                    msg = "Invalid Message type"
                    raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def post_validation(self):
        match self.type:
            case SupportedWSEvent.UPVOTE.value:
                self.details = UpvoteMessage(**self.details.model_dump())
            case SupportedWSEvent.CONFESSION.value:
                self.details = ConfessionMessage(**self.details.model_dump())
            case SupportedWSEvent.COMMENT.value:
                self.details = CommentMessage(**self.details.model_dump())
            case _:
                msg = "Invalid Message type"
                raise ValueError(msg)
        return self
