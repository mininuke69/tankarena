from socket import socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
from math import sqrt
from pydantic import BaseModel
from typing import Optional
from typing import List
from time import perf_counter
from time import sleep

"""
notes: 
- every update cycle, update each object with its momentum

"""


class Vector2:
    # todo:
    # -normalize()
    # -cut() (normalize, unless vector is shorter)

    def __init__(self, x = 0, y = 0) -> None:
        self.x = x
        self.y = y


    def magnitude(self):
        return sqrt(self.x ** 2 + self.y ** 2)
    



class SceneObject:
    def __init__(self, x: int, y: int, width: int, height: int, momentum: Vector2) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.momentum = momentum

    
    def update_position_cycle(self):
        self.x += self.momentum.x
        self.y += self.momentum.y


class Tank(SceneObject):
    def __init__(self, x: int, y: int, width: int, height: int, momentum: Vector2, nick = "guest") -> None:
        super().__init__(x, y, width, height, momentum)
        self.nick = nick


class Bullet(SceneObject):
    def __init__(self, x: int, y: int, width: int, height: int, momentum: Vector2, shooter: Tank) -> None:
        self.shooter = shooter
        super().__init__(x, y, width, height, momentum)


class Wall(SceneObject):
    def __init__(self, x: int, y: int, width: int, height: int, momentum: Vector2) -> None:
        super().__init__(x, y, width, height, momentum)











def handle_client(sock: socket, addr: str):
    global scene_objects


    class Command(BaseModel):
        command: str
        nick: Optional[str]
        x: Optional[int]
        y: Optional[int]

    """
    class Player:
        def __init__(self, nick = "guest", x = 0, y = 0) -> None:
            self.nick = nick
            self.x, self.y = x, y
    """


    player = Tank(x=0, y=0, width=10, height=10, momentum=Vector2(0, 0))
    while True:
        data = Command(sock.recv(512).decode())

        if data.command == "move": 
            ## todo: make reference to SceneObject instead of saving in Player class
            move_vector = Vector2(data.x, data.y)
            move_vector.cut(max_magnitude=15)

            player.x += data.x
            player.y += data.y

        elif data.command == "shoot":
            scene_objects.append(Bullet())


def handle_update_cycle(update_speed = 25):
    global scene_objects

    while True:

        start = perf_counter()

        for scene_object in scene_objects:
            scene_object.update_position_cycle()

        end = perf_counter()

        sleep(1/update_speed - (end - start))
        print("cycle completed")


server = socket(family=AF_INET, type=SOCK_STREAM)

scene_objects: List[SceneObject] = []



Thread(target=handle_update_cycle, args=(10,)).start()

while True:
    sock, addr = server.accept()
    Thread(target=handle_client, args=(sock, addr)).start()