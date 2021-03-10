from flask_sqlalchemy import SQLAlchemy
from . import db
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous.url_safe import URLSafeSerializer
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# it is a test
def token_required(func):
    def wrapper(*args, **kwargs):
        print("There we go")
        
        return func(*args, **kwargs)

    return wrapper

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    # admin = db.Column(db.Boolean, default=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.admin

    def generate_token(self, expires=18000):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires)
        token = s.dumps({'email': self.email})
        return token

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.Text, nullable=True)
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
