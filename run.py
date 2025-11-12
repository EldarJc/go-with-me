from app import create_app
from config import BaseConfig

app = create_app(BaseConfig)


if __name__ == "__main__":
    app.run()
