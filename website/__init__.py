from flask import Flask
from datetime import timedelta
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"
STORAGE = 1000


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "ThisISmySecretKey"
    app.permanent_session_lifetime = timedelta(minutes=5)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import Views
    from .auth import Auth
    from .admin import admin
    from .adding import adding

    app.register_blueprint(Views, url_prefix="/")
    app.register_blueprint(Auth, url_prefix="/")
    app.register_blueprint(admin, url_prefix="/")
    app.register_blueprint(adding, url_prefix="/")

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists(DB_NAME):
        with app.app_context():
            db.create_all()