import os

from dotenv import load_dotenv

load_dotenv()

base_dir = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.join(base_dir, "instance")


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "app_secret_key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_ENGINE", "sqlite:///") + os.path.join(
        instance_dir, "test_data.db"
    )


class DevConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    TESTING = True
