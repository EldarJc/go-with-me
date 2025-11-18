from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, model, utc_now
from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(40), nullable=False)
    last_name: Mapped[str] = mapped_column(String(40), nullable=False)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    bio: Mapped[str] = mapped_column(String(350), default="No bio")
    owned_groups: Mapped[list["Group"]] = relationship(
        "Group", back_populates="owner", cascade="all, delete-orphan", lazy="selectin"
    )
    owned_events: Mapped[list["Event"]] = relationship(
        "Event", back_populates="owner", cascade="all, delete-orphan", lazy="selectin"
    )
    events: Mapped[list["EventAttendee"]] = relationship(
        "EventAttendee",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @property
    def password(self) -> None:
        raise AttributeError("Password is write-only")

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)


group_tags = db.Table(
    "group_tags",
    db.Column("group_id", db.Integer, db.ForeignKey("groups.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


class Group(BaseModel):
    __tablename__ = "groups"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500), default="No description")
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    owner: Mapped["User"] = relationship("User", back_populates="owned_groups")
    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary=group_tags,
        back_populates="groups",
        lazy="selectin",
    )


class GroupMember(model):
    __tablename__ = "group_members"

    group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    __table_args__ = PrimaryKeyConstraint("group_id", "user_id", name="pk_group_user")


class Location(BaseModel):
    __tablename__ = "locations"
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    events: Mapped[list["Event"]] = relationship(
        "Event",
        back_populates="location",
        lazy="selectin",
        cascade="all, delete-orphan",
    )


event_tags = db.Table(
    "events_tags",
    db.Column("event_id", db.Integer, db.ForeignKey("events.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


class Event(BaseModel):
    __tablename__ = "events"

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="No description")
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    mode: Mapped[str] = mapped_column(String, nullable=False)
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    owner: Mapped["User"] = relationship("User", back_populates="owned_events")
    group_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("groups.id", ondelete="CASCADE", name="fk_event_group"),
        nullable=True,
    )
    attendees: Mapped[list["EventAttendee"]] = relationship(
        "EventAttendee", back_populates="event", lazy="selectin"
    )

    location_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("locations.id", nullable=False)
    )
    location: Mapped["Location"] = relationship("Location", back_populates="events")

    tags: Mapped[list["Tag"]] = relationship(
        "Tag", secondary=event_tags, back_populates="events", lazy="selectin"
    )


class EventAttendee(model):
    __tablename__ = "event_attendees"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="events")
    event: Mapped["Event"] = relationship("Event", back_populates="attendees")

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "event_id", name="pk_user_event"),
    )


class Tag(BaseModel):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    events: Mapped[list["Event"]] = relationship(
        "Event", secondary=event_tags, back_populates="tags", lazy="selectin"
    )
    groups: Mapped[list["Group"]] = relationship(
        "Group", secondary=group_tags, back_populates="tags", lazy="selectin"
    )
