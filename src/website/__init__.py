from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from environs import Env

env = Env()
env.read_env()

db = SQLAlchemy()
MYSQL_USERNAME = env("MYSQL_USERNAME")
MYSQL_PASSWORD = env("MYSQL_PASSWORD")
MYSQL_HOST = env("MYSQL_HOST")
MYSQL_PORT = env.int("MYSQL_PORT")
MYSQL_DATABASE = "CSET160_FINAL_PROJECT"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = env("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app
