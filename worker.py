import pika
import json
import random
import time
from models import db, Task


def process_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.status = 'IN_PROGRESS'
        db.session.commit()
        print(f"Task {task_id} is now IN_PROGRESS")

        time.sleep(random.randint(5, 10))

        if random.random() > 0.2:  # 80% шанс на успех
            task.status = 'COMPLETED'
        else:
            task.status = 'ERROR'

        db.session.commit()
        print(f"Task {task_id} processed with status: {task.status}")
    else:
        print(f"Task {task_id} not found!")


def callback(ch, method, properties, body):
    task_data = json.loads(body)
    task_id = task_data['task_id']
    print(f" [x] Received task: {task_id}")
    process_task(task_id)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume_tasks_from_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    print(' [*] Waiting for tasks. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    consume_tasks_from_queue()
