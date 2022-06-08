from abc import ABC, abstractmethod
from os import system
from PodSixNet.Connection import ConnectionListener, connection

from entities import Player


class BaseScene(ABC):
    def __init__(self, network_client):
        self._network_client = network_client
        self._scene = self
        self._waiting_for_response = False

    @abstractmethod
    def handle_network(self, data):
        pass

    @abstractmethod
    def execute_scene(self):
        pass

    def _wait_network_result(self):
        self._waiting_for_response = True
        while self._waiting_for_response:
            connection.Pump()
            self._network_client.Pump()


class MainMenuScene(BaseScene):
    def execute_scene(self):
        print("Ular tangga")
        print("By:")
        print("mirzaq19 and zydhanlinnar11")
        print("1. Create Room")
        print("2. Join Room")
        inp = input()
        while int(inp) not in [1, 2]:
            print('seng nggenah blog')
            inp = input()
        scene: BaseScene
        if inp == '1':
            scene = CreateRoomScene(self._network_client)
        else:
            scene = JoinRoomScene(self._network_client)
        self._network_client.change_scene(scene)
        scene.execute_scene()

    def handle_network(self, data):
        pass


class CreateRoomScene(BaseScene):
    def execute_scene(self):
        system('cls')
        self._network_client.Send({'action': 'createroom'})
        self._wait_network_result()

    def handle_network(self, data):
        if data['action'] == 'createroomresponse':
            self._waiting_for_response = False
            room_id = data['roomid']
            print(f'Room Code: {room_id}')
            self._wait_network_result()
        elif data['action'] == 'playgame':
            self._waiting_for_response = False
            scene = InGameScene(self._network_client)
            self._network_client.change_scene(scene)
            scene.execute_scene()


class JoinRoomScene(BaseScene):
    def __request_room_id(self):
        room_id = input("Enter room code: ")
        self._network_client.Send({'action': 'joinroom', 'room_id': room_id})
        self._wait_network_result()

    def execute_scene(self):
        system('cls')
        self.__request_room_id()

    def handle_network(self, data):
        if data['action'] == 'joinroomerror':
            system('cls')
            print(data['message'])
            self.__request_room_id()
        elif data['action'] == 'playgame':
            self._waiting_for_response = False
            scene = InGameScene(self._network_client)
            self._network_client.change_scene(scene)
            scene.execute_scene()


class InGameScene(BaseScene):
    def execute_scene(self):
        system('cls')
        print("waiting for network")
        self._wait_network_result()

    def handle_network(self, data):
        if data['action'] == 'playgameinfo':
            self._waiting_for_response = False
            # system('cls')
            player = Player(data['player_id'])
            opponent = Player(data['opponent_id'])
            print(data)
