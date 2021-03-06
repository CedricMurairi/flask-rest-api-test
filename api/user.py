from flask import Blueprint

user = Blueprint('user', __name__)

@user.route('/users', methods=['POST'])
def register():
    pass