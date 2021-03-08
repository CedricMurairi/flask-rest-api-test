from flask import Blueprint, request, abort
from .models import User
from . import db
from .task import make_public

user = Blueprint('user', __name__)

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

    new_use = User(name='Cedric', email=email, password=password)
    db.session.add(new_use)
    db.session.commit()

    return {'message': 'User created successfully'}, 200

# @user.route('/todo/api/v1.0/users', methods=['GET'])
# def login():
#     if not request.authorization:
#         abort(400)

#     email = request.authorization.username
#     password = request.authorization.password
#     user = User.query.filter(email=email)

#     if user and user.verify_password(password):
#         return {'message': 'Login successfull', 'data':
#             {
#                 'id': user.id,
#                 'username': user.name,
#                 'email': user.email,
#                 'tasks': [make_public(taks) for taks in user.tasks]
#             }
#         }

#     abort(400)

@user.route('/todo/api/v1.0/users', methods=['GET'])
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
    ]}

@user.route('/todo/api/v1.0/users/<int:id>', methods=['PUT'])
# @login_required
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

@user.route('/todo/api/v1.0/users<int:id>', methods=['DELETE'])
# @login_required
# admin_required
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return {'error': 'User does not exist'}, 404

    db.session.delete(user)
    db.session.commit()

    