from tornado import websocket
import myamqp
import urllib
import json
import random
import time

sockets = []
origins = []
rooms = {}
current = 1

def broadcast(message):
    for room in rooms.values():
        for socket in room.values():
            socket.write_message(message)

def generateRoom():
    global current
    while (str(current).zfill(4) in rooms):
        current += 1
        if current > 9999:
            current = 1
    room = str(current).zfill(4)
    current += 1
    if current > 9999:
        current = 1
    return room

class WsHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        parsed_origin = urllib.parse.urlparse(origin)
        if parsed_origin.netloc.endswith("yifanma.me") or parsed_origin.netloc.startswith("localhost"):        
            # if parsed_origin.netloc in origins:
            #     return False
            # else:
            self.origin = parsed_origin.netloc
                # origins.append(parsed_origin.netloc)
            return True
        return False
    
    def on_message(self, inMessage):
        message = json.loads(inMessage)
        type = message["type"]
        if type == "create":
            room = generateRoom()
            rooms[room] = {}
            rooms[room]["host"] = self
            self.room = room
            self.write_message(json.dumps({
                "type": "create",
                "room": room
            }))
            if len(rooms[room].keys()) == 2:
                firstColour = "black" if random.randint(0, 1) == 0 else "white"
                secondColour = "black" if firstColour == "white" else "white"
                rooms[room]["host"].write_message(json.dumps({
                    "type": "ready",
                    "colour": firstColour
                }))
                rooms[room]["host"].colour = firstColour
                rooms[room]["client"].write_message(json.dumps({
                    "type": "ready",
                    "colour": secondColour
                }))
                rooms[room]["client"].colour = secondColour
        elif type == "join":
            room = message["room"]
            if room in rooms:
                rooms[room]["client"] = self
                self.room = room
                self.write_message(json.dumps({
                    "type": "join",
                    "room": room
                }))
                if len(rooms[room].keys()) == 2:
                    firstColour = "black" if random.randint(0, 1) == 0 else "white"
                    secondColour = "black" if firstColour == "white" else "white"
                    rooms[room]["host"].write_message(json.dumps({
                        "type": "ready",
                        "colour": firstColour
                    }))
                    rooms[room]["host"].colour = firstColour
                    rooms[room]["client"].write_message(json.dumps({
                        "type": "ready",
                        "colour": secondColour
                    }))
                    rooms[room]["client"].colour = secondColour
        elif type == "username":
            self.username = message["username"]
            myamqp.createUser(message["username"])
            myamqp.updatePlayer(message["username"])
        elif type == "num_online":
            myamqp.onlinePlayers()
        elif type == "move":
            room = message["room"]
            x = message["data"]["x"]
            y = message["data"]["y"]
            colour = message["data"]["colour"]
            for socket in rooms[room].values():
                socket.write_message(json.dumps({
                    "type": "move",
                    "colour": colour,
                    "x": x,
                    "y": y
                }))
        elif type == "game_finished":
            winner = message["winner"]
            for socket in rooms[self.room].values():
                myamqp.matchResult(socket.username, socket.colour, "win" if socket.colour == winner else "loss")
                myamqp.updatePlayer(socket.username)
            time.sleep(5)
            for socket in rooms[self.room].values():
                firstColour = "black" if random.randint(0, 1) == 0 else "white"
                secondColour = "black" if firstColour == "white" else "white"
                rooms[self.room]["host"].write_message(json.dumps({
                    "type": "ready",
                    "colour": firstColour
                }))
                rooms[self.room]["host"].colour = firstColour
                rooms[self.room]["client"].write_message(json.dumps({
                    "type": "ready",
                    "colour": secondColour
                }))
                rooms[self.room]["client"].colour = secondColour
            
    def on_close(self):
        if self.room and self.room in rooms:
            del rooms[self.room]
        # if self.origin in origins:
        #     origins.remove(self.origin)
