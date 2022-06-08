from random import choices
from string import ascii_uppercase, digits
from time import sleep
from typing import Tuple
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

SERVER_HOST: "str" = "localhost"
SERVER_PORT: "int" = 5071

available_room: 'list[str]' = []
rooms: 'dict[str, list[ClientChannel]]' = {}


class ClientChannel(Channel):
    def Network(self, data):
        pass

    def Network_createroom(self, data: 'dict'):
        print(data)
        room_id = ''.join(choices(ascii_uppercase + digits, k=6))
        while room_id in available_room:
            room_id = ''.join(choices(ascii_uppercase + digits, k=6))
        self.Send({'action': 'createroomresponse', 'roomid': room_id})
        available_room.append(room_id)
        rooms[room_id] = []
        rooms[room_id].append(self)

    def Network_deleteroom(self, data: 'dict'):
        room_id = data.get('room_id')
        try:
            rooms.pop(room_id)
            available_room.remove(room_id)
        except ValueError:
            pass
        except KeyError:
            pass

    def Network_joinroom(self, data: 'dict'):
        room_id = data.get('room_id')
        is_room_exist = room_id in available_room and room_id in rooms
        if not is_room_exist:
            self.Send({'action': 'joinroomerror',
                      'message': "Room doesn't exist"})
            return
        if len(rooms[room_id]) != 1:
            self.Send({'action': 'joinroomerror',
                      'message': "Room is full"})
            return
        rooms[room_id].append(self)
        for channel in rooms[room_id]:
            channel.Send({'action': 'playgame', 'room_id': room_id})


class GameServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)

    def Connected(self, channel: 'ClientChannel', addr: 'Tuple[str, int]'):
        print("new connection:", channel)


if __name__ == '__main__':
    server = GameServer(localaddr=(SERVER_HOST, SERVER_PORT))

    while True:
        server.Pump()
        sleep(0.0001)
