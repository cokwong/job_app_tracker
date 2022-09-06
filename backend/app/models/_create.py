from flask import Flask
import sqlalchemy
import os

from dotenv import load_dotenv
load_dotenv()


def create():
    """

    """
    engine = sqlalchemy.create_engine(
                f'mysql+pymysql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWD")}@{os.getenv("DB_HOST")}'
            )
    engine.execute("CREATE DATABASE IF NOT EXISTS job_tracker")

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'mysql+pymysql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from models import db

    db.init_app(app)
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    create()
