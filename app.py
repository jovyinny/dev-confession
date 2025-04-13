"""Entry point."""

from src.api import app

if __name__ == "__main__":
    # If its run as script
    import uvicorn

    uvicorn.run(app)
