import myamqp
import mysocket
from tornado import web, ioloop
import signal
from threading import Thread

app = web.Application([
    (r'/ws', mysocket.WsHandler)
])

if __name__ == '__main__':
    app.listen(8888)
    print("started on 8888")
    thread = Thread(target=myamqp.receive)
    thread.start()
    print("rabbit started")
    myamqp.onlinePlayers()
    ioloop.IOLoop.instance().start()
