import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DB_PATH"]


class DevConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    TESTING = True
