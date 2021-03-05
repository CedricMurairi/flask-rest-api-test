#!flask/bin/python
from flask import Flask, abort, request, url_for

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'You should buy milk, sugar, lemon, tomatos and more',
        'done': False
    },
    {
        'id': 2,
        'title': u'Do the cookings',
        'description': u'You should cook you mom\'s favourite dish, your dad\'s and you friends\'',
        'done': False
    }
]

@app.errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404

@app.errorhandler(400)
def bad_request(error):
    return {'error': 'Bad request'}, 400

@app.route("/todo/api/v1.0/tasks", methods=['POST'])
def add_task():
    if not request.json or not 'title' in request.json:
        abort(400)

    task_title = request.json['title']
    task_description = request.json.get('description', "")

    new_task = {'id': tasks[-1]['id'] + 1, 'title': task_title, 'description': task_description, 'done': False}
    tasks.append(new_task)
    return {'task': make_public(new_task)}, 201

@app.route("/todo/api/v1.0/tasks/<int:id>", methods=['DELETE'])
def delete_task(id):
    for task in tasks:
        if task['id'] == id:
            tasks.remove(task)
            return {'taks': make_public(task)}, 200
    abort(404)

@app.route("/todo/api/v1.0/tasks/<int:id>", methods=['PUT'])
def update_task(id):
    if not request.json:
        abort(400)

    for task in tasks:
        if task['id'] == id:
            title = request.json.get('title', task['title'])
            description = request.json.get('description', task['description'])            
            done = request.json.get('done', task['done'])
            if type(done) is not bool:
                aboart(400)

            task['title'] = title
            task['description'] = description
            task['done'] = done
            return {'task': make_public(task)}, 200
    abort(404)

@app.route("/todo/api/v1.0/tasks/<int:id>", methods=['GET'])
def get_task(id):
    for task in tasks:
        if task['id'] == id:
            return {'task': make_public(task)}
    abort(404)

@app.route("/todo/api/v1.0/tasks", methods=['GET'])
def get_tasks():
    return {'tasks': [make_public(task) for task in tasks]}

def make_public(task):
    new_task = {}

    for item in task:
        if item == 'id':
            new_task['uri'] = url_for('get_task', id=task['id'], _external=True)
        else:
            new_task[item] = task[item]
    return new_task

if __name__ == "__main__":
    app.run(debug=True)
