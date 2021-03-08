from flask import Flask, abort, request, url_for, Blueprint
from .models import Task
from . import db

task = Blueprint('task', __name__)


@task.errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404

@task.errorhandler(400)
def bad_request(error):
    return {'error': 'Bad request'}, 400

@task.errorhandler(500)
def server_error(error):
    return {'error': 'Internal server error'}, 500

@task.route("/todo/api/v1.0/tasks", methods=['POST'])
def add_task():
    if not request.json or not 'title' in request.json:
        abort(400)

    task_title = request.json['title']
    task_description = request.json.get('description', "")

    new_task = Task(title=task_title, description=task_description, done=False, user_id=1)
    db.session.add(new_task)
    db.session.commit()
    return {'task': make_public(new_task)}, 201

@task.route("/todo/api/v1.0/tasks/<int:id>", methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        abort(404)

    db.session.delete(task)
    db.session.commit()

    return {'task': make_public(task)}, 200

@task.route("/todo/api/v1.0/tasks/<int:id>", methods=['PUT'])
def update_task(id):
    if not request.json:
        abort(400)

    task = Task.query.get(id)
    if not task:
        abort(404)

    title = request.json.get('title', task.title)
    description = request.json.get('description', task.description)            
    done = request.json.get('done', bool(task.done))
    if type(done) is not bool:
        abort(400)

    task.title = title
    task.description = description
    task.done = done

    db.session.commit()

    return {'task': make_public(task)}, 200

@task.route("/todo/api/v1.0/tasks/<int:id>", methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    if not task:
        abort(404)

    return {'task': make_public(task)}

@task.route("/todo/api/v1.0/tasks", methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return {'tasks': [make_public(task) for task in tasks]}

def make_public(task):
    new_task = {}

    new_task['title'] = task.title
    new_task['description'] = task.description
    new_task['done'] = bool(task.done)
    new_task['user_id'] = task.user_id
    new_task['uri'] = url_for('task.get_task', id=task.id, _external=True)

    return new_task
