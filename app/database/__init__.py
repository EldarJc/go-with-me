from datetime import datetime, timezone
from typing import TYPE_CHECKING

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

db_migrate = Migrate()


if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model

    model = Model
else:
    model = db.Model


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
