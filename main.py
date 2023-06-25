import os
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_URI = os.environ.get("DATABASE_URI")


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    @app.route("/")
    def index():
        return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

    return app


if __name__ == "__main__":
    app = create_app()

    app.run(
        debug=True if os.getenv("FLASK_DEBUG") else False,
        port=os.getenv("PORT", default=5000),  # type: ignore
    )
