from tornado import websocket
import urllib
import uuid

sockets = []
origins = []

class WsHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        parsed_origin = urllib.parse.urlparse(origin)
        if parsed_origin.netloc.endswith("yifanma.me") or parsed_origin.netloc.startswith("localhost"):        
            if parsed_origin.netloc in origins:
                return False
            else:
                self.origin = parsed_origin.netloc
                origins.append(parsed_origin.netloc)
                return True
        return False

    def open(self):
        if self not in sockets:
            sockets.append(self)
    
    def on_message(self, message):
        for socket in sockets:
            socket.write_message(message)

    def on_close(self):
        if self in sockets:
            sockets.remove(self)
        if self.origin in origins:
            origins.remove(self.origin)
