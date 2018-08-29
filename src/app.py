import myamqp
import mysocket
from tornado import web, ioloop
import signal

app = web.Application([
    (r'/ws', mysocket.WsHandler)
])

if __name__ == '__main__':
    app.listen(8888)
    print('started on 8888')
    ioloop.IOLoop.instance().start()
