from flask import Blueprint, request, abort, make_response, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .models import User, token_required
from . import db
from .task import make_public
from sqlalchemy import or_

user = Blueprint('user', __name__)

@user.errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404

@user.errorhandler(400)
def bad_request(error):
    return {'error': 'Bad request'}, 400

@user.errorhandler(500)
def server_error(error):
    return {'error': 'Internal server error'}, 500

@user.route('/todo/api/v1.0/users', methods=['POST'])
def register():
    if not request.authorization:
        abort(400)

    email = request.authorization.username
    username = email.split('@')[0]
    password = request.authorization.password

    user = User.query.filter_by(email=email).first()
    if user:
       return {'error': 'User mail already exist'}, 400

    new_use = User(name=username, email=email, password=password)
    db.session.add(new_use)
    db.session.commit()

    return {'message': 'User created successfully'}, 200

@user.route('/todo/api/v1.0/users', methods=['GET'])
def login():
    if not request.authorization:
        abort(400)

    username = request.authorization.username
    password = request.authorization.password
    user = User.query.filter(or_(User.email==username, User.name==username)).first()

    if user and user.verify_password(password):
        s = Serializer(current_app.config['SECRET_KEY'])

        token = user.generate_token()
        print(token)
        try:
            data = s.loads(token)
            print(data)
        except Exception as e:
            print("No data ", e)

        return {'message': 'Login successfull', 'data':
            {
                'id': user.id,
                'username': user.name,
                'email': user.email,
                'token': token,
                'tasks': [make_public(taks) for taks in user.tasks]
            }
        }

    abort(404)

@user.route('/todo/api/v1.0/users/<int:id>', methods=['GET'])
# @token_required
def get_user(id):
    user = User.query.get(id)

    if not user:
        abort(404)

    return {'user':
        {
            'id': user.id,
            'username': user.name,
            'email': user.email,
            'tasks': [make_public(taks) for taks in user.tasks]
        }
    }, 200

@user.route('/todo/api/v1.0/users/all', methods=['GET'])
# @admin_required
def get_users():
    users = User.query.all()

    return {'users': [
        {
            'id': user.id,
            'username': user.name,
            'email': user.email,
            'tasks': [make_public(taks) for taks in user.tasks]
        } for user in users
    ]}, 200

@user.route('/todo/api/v1.0/users/<int:id>', methods=['PUT'])
# @login_required and admin_can
def update_user(id):
    user = User.query.get(id)

    if not user:
        return {'error': 'User do not exist'}, 400
    
    if not request.json:
        abort(400)

    email = request.json['email', user.email]
    username = request.json['username', user.name]

    if User.query.filter_by(email=email):
        return {'error': 'User email aready exists'}, 400

    user.email = email
    user.username = username

    return {'message': 'User updated succesfully'}

@user.route('/todo/api/v1.0/users/<int:id>', methods=['DELETE'])
# @login_required
# @admin_required
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return {'error': 'User does not exist'}, 404

    db.session.delete(user)
    db.session.commit()

    return {'message': 'User deleted succefully'}

    