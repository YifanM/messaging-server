import pika
import json

queueName = 'gomoku';
queueNameToClient = queueName + 'ToClient';
queueNameToServer = queueName + 'ToServer';

def createUser(username):
    send("CREATE_USER", { "username": username })

def matchResult(username, colour, result):
    send("MATCH_RESULT", { "username": username, "colour": colour, "result": result })

def onlinePlayers():
    send("ONLINE_PLAYERS", {})

def updatePlayer():
    send("UPDATE_PLAYER", { "username": username })

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
