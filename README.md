# tankarena
a tank battle arena framework/lib 






1. server with simulation
2. lib to interface with server
3. demo client



### game

- 1 shot/s
- no bouncing
- no explosions
- 5 hp
- med ==> +1 hp
- tank size = 10x10
- bullet size = 1x1
- tank speed = 5
- bullet speed = 15
- tank speed and bullet speeds are normalized
- no changing lib
- no tank-tank collision, only wall-tank collision




### server
- simulation in real time
- connecting to clients handled by lib client-side and integrated server-side
- fuck security
- normalize received tank and bullet vectors
- players and bots can join at any time and directly start playing, no pauses (yet)
- 25hz updates (goal)







### lib

- connection using server name or ip
- auth using nick
- send requests using functions:

----
from tankarena.client import Client
client = Client()
client.connect(nick="nik", host="192.168.88.8")

client.update()
x = client.x
inview = client.visible
health = client.health

client.shoot(2, 2)
----



- wrapper for sending requests
- no auto update for getting info
- request is sent on function call
- no async/await bs
- every send call, the player sends an action, without coordinates or nickname
commands are:

nick(nick: str) ==> changes nickname
move(x: int, y: int) ==> moves by a certain amount
shoot(x: int, y: int) ==> shoots in certain direction