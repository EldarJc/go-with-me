import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, PrimaryKeyConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import db

dt = datetime.datetime


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    first_name: Mapped[str] = mapped_column(String(40))
    last_name: Mapped[str] = mapped_column(String(40))
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[dt] = mapped_column(
        DateTime, default=lambda: dt.now(datetime.timezone.utc)
    )
    bio: Mapped[str] = mapped_column(String(350), default="No bio")
    owned_groups: Mapped[list["Group"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )
    owned_events: Mapped[list["Event"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )
    events: Mapped[list["EventAttendee"]] = relationship(
        "EventAttendee", back_populates="user"
    )


class Group(db.Model):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String(500), default="No description")
    created_at: Mapped[dt] = mapped_column(
        DateTime, default=lambda: dt.now(datetime.timezone.utc)
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    owner: Mapped["User"] = relationship("User", back_populates="owned_groups")


class GroupMember(db.Model):
    __tablename__ = "group_members"

    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    joined_at: Mapped[dt] = mapped_column(
        DateTime, default=lambda: dt.now(datetime.timezone.utc)
    )

    __table_args__ = PrimaryKeyConstraint("group_id", "user_id", name="pk_group_user")


class Location(db.Model):
    __tablename__ = "locations"
    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(String(100))
    latitude: Mapped[float] = mapped_column(nullable=True)
    longitude: Mapped[float] = mapped_column(nullable=True)
    event_locations: Mapped[list["EventLocation"]] = relationship(
        "EventLocation", back_populates="location"
    )


class Event(db.Model):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(Text, default="No description")
    start_date: Mapped[dt] = mapped_column(DateTime, nullable=False)
    mode: Mapped[str] = mapped_column(nullable=False)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    owner: Mapped["User"] = relationship("User", back_populates="owned_events")
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE", name="fk_event_group"),
        nullable=True,
    )
    created_at: Mapped[dt] = mapped_column(
        DateTime, default=lambda: dt.now(datetime.timezone.utc)
    )
    attendees: Mapped[list["EventAttendee"]] = relationship(
        "EventAttendee", back_populates="event"
    )

    locations: Mapped[list["EventLocation"]] = relationship(
        "EventLocation", back_populates="event"
    )


class EventLocation(db.Model):
    __tablename__ = "event_locations"

    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id", ondelete="CASCADE")
    )
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))

    event: Mapped["Event"] = relationship("Event", back_populates="locations")
    location: Mapped["Location"] = relationship(
        "Location", back_populates="event_locations"
    )

    __table_args__ = (
        PrimaryKeyConstraint("event_id", "location_id", name="pk_event_location"),
    )


class EventAttendee(db.Model):
    __tablename__ = "event_attendees"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )
    joined_at: Mapped[dt] = mapped_column(
        DateTime, default=lambda: dt.now(datetime.timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="events")
    event: Mapped["Event"] = relationship("Event", back_populates="attendees")

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "event_id", name="pk_user_event"),
    )
