import pickle
from random import choices
import random
from string import ascii_uppercase, digits
from time import sleep
from typing import Tuple
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

from entities import Dice, Player

SERVER_HOST: "str" = "localhost"
SERVER_PORT: "int" = 5071

available_room: 'list[str]' = []
rooms: 'dict[str, list[ClientChannel]]' = {}


class ClientChannel(Channel):
    def Network(self, data):
        pass

    def Network_createroom(self, data: 'dict'):
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
        self.__start_game(room_id)

    def Network_rolldice(self, data: 'dict'):
        dice_result = Dice().roll()
        room_id = data['room_id']
        channels = rooms[room_id]
        next_turn: 'str' = ''
        for channel in channels:
            if f'{channel.addr[0]}:{str(channel.addr[1])}' != f'{self.addr[0]}:{str(self.addr[1])}':
                next_turn = f'{channel.addr[0]}:{str(channel.addr[1])}'
                break
        for channel in channels:
            channel.Send({'action': 'diceresult', 'data': str(
                dice_result), 'current_turn_player_id': next_turn})

    def __start_game(self, room_id: 'str'):
        channels = rooms[room_id]
        first_turn = random.choice(channels)
        player_ids: 'list[str]' = []
        for channel in channels:
            player_ids.append(f'{channel.addr[0]}:{str(channel.addr[1])}')
        for channel in channels:
            opponent_id = player_ids[0]
            if player_ids[0] == f'{channel.addr[0]}:{str(channel.addr[1])}':
                opponent_id = player_ids[1]
            channel.Send({'action': 'playgameinfo',
                          'player_id': f'{channel.addr[0]}:{str(channel.addr[1])}',
                          'opponent_id': opponent_id,
                          'current_turn_player_id': f'{first_turn.addr[0]}:{str(first_turn.addr[1])}',
                          'room_id': room_id})


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
