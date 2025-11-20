from enum import Enum


class GroupRole(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class EventRole(Enum):
    ORGANIZER = "organizer"
    SPEAKER = "speaker"
    PARTICIPANT = "participant"
