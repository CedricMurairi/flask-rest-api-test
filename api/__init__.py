from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(32)

    from .user import user
    from .task import task

    app.register_blueprint(user, url_prefix='/')
    app.register_blueprint(task, url_prefix='/')

    db.init_app(app)
    CORS(app)

    create_db(app)

    return app

def create_db(app):
    if not os.path.exists('api/base.db'):
        db.create_all(app=app)
