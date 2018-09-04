import myamqp
import mysocket
from tornado import web, ioloop
import signal
import asyncio
from threading import Thread

app = web.Application([
    (r'/ws', mysocket.WsHandler)
])

def start_amqp():
    asyncio.set_event_loop(asyncio.new_event_loop())
    myamqp.receive()

if __name__ == '__main__':
    app.listen(8888)
    print("started on 8888")
    thread = Thread(target=start_amqp)
    thread.start()
    print("rabbit started")
    myamqp.onlinePlayers()
    ioloop.IOLoop.instance().start()
