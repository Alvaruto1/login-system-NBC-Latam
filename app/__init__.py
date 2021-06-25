import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_migrate import Migrate
from app.models.models import db, User
from app.controllers.auth import auth
from app.controllers.user import user
migrate = Migrate()


POSTGRES = {
    'user': os.environ['POSTGRES_USER'],
    'pw': os.environ['POSTGRES_PASSWORD'],
    'db': os.environ['POSTGRES_DB'],
    'host': os.environ['POSTGRES_HOST'],
    'port': os.environ['POSTGRES_PORT'],
}


def create_app():
    app = Flask(__name__, static_folder="./views/statics")

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES["user"]}:{POSTGRES["pw"]}@{POSTGRES["host"]}:{POSTGRES["port"]}/{POSTGRES["db"]}'
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(user)

    app.app_context().push()
    db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/',)
    def signup_post():
        return redirect(url_for('auth.login'))

    @app.errorhandler(404)
    def page_not_found(error):
        return redirect(url_for('auth.login'))

    return app

