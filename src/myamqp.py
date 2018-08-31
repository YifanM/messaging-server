import pika
import json

queueName = 'gomoku';
queueNameToClient = queueName + 'ToClient';
queueNameToServer = queueName + 'ToServer';

def send(type, content):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queueNameToServer)
    channel.basic_publish(exchange='', routing_key=queueNameToServer, body=json.dumps({
        "type": type,
        "content": content
    }))
    connection.close()

def received(channel, method, properties, message):
    print(json.loads(message))

def receive():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queueNameToClient)
    channel.basic_consume(received, queue=queueNameToClient, no_ack=True)
    channel.start_consuming()
