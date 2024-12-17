from flask_restful import Resource
from flask import request
from models import Task, db
from message_queue import send_task_to_queue

class TaskListResource(Resource):
    def get(self):
        status = request.args.get('status')
        if status:
            tasks = Task.query.filter_by(status=status).all()
        else:
            tasks = Task.query.all()
        return [task.to_dict() for task in tasks], 200

    def post(self):
        data = request.get_json()
        description = data['description']
        task = Task(description=description, status='NEW')
        db.session.add(task)
        db.session.commit()
        send_task_to_queue({'task_id': task.id, 'description': task.description})

        return task.to_dict(), 201


class TaskResource(Resource):
    def get(self, id):
        task = Task.query.get_or_404(id)
        return task.to_dict(), 200
