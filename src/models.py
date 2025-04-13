"""Project Models."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from uuid import UUID

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

from src.schemas import ConfessionMessage

sqlite_path = Path(__file__).parent / "database.db"
engine = create_engine(url=f"sqlite:///{sqlite_path!s}")


class Confession(SQLModel, table=True):
    """Confession table."""

    id: UUID = Field(
        primary_key=True,
    )
    text: str
    upvotes: Optional[int] = Field(  # noqa: FA100
        default=0,
        sa_column_kwargs={"server_default": "0"},
        description="Upvote counts.",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc),
    )
    # Relationship
    comments: list["Comment"] = Relationship(
        back_populates="confession",
    )
    files: list["File"] = Relationship(
        back_populates="confession",
    )

    @classmethod
    def create_confession(
        cls,
        message: ConfessionMessage,
    ) -> "Confession":
        """Add confession."""
        with Session(engine) as session:
            confession = cls(**message.model_dump())
            session.add(confession)
            session.commit()
            session.refresh(confession)
            return confession

    @classmethod
    def upvote_confession(
        cls,
        *,
        confession_id: UUID,
    ) -> Optional["Confession"]:
        """Upvode Confession."""
        with Session(engine) as session:
            confession = session.exec(
                select(cls).where(cls.id == confession_id),
            ).first()
            if not confession:
                return None
            confession.upvotes += 1
            return confession


class Comment(SQLModel, table=True):
    """Confession comments."""

    id: Optional[int] = Field(  # noqa: FA100
        primary_key=True,
        default=None,
    )
    confession_id: UUID = Field(
        foreign_key="confession.id",
    )
    text: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc),
    )
    # Relationship
    confession: Confession = Relationship(
        back_populates="comments",
    )
    files: list["File"] = Relationship(
        back_populates="comment",
    )


class File(SQLModel, table=True):
    """Mdeia."""

    id: Optional[int] = Field(  # noqa: FA100
        primary_key=True,
        default=None,
    )
    name: str = Field(
        description="Media name.",
    )
    confession_id: UUID = Field(
        foreign_key="confession.id",
    )
    comment_id: int = Field(
        foreign_key="comment.id",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc),
    )
    # Relationship
    comment: Comment = Relationship(
        back_populates="files",
    )
    confession: Confession = Relationship(
        back_populates="files",
    )


SQLModel.metadata.create_all(engine)
