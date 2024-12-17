import pika
import json

def send_task_to_queue(task_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=json.dumps(task_data),
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
    print(f" [x] Sent task to queue: {task_data}")
    connection.close()
