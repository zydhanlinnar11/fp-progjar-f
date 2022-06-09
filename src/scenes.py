from abc import ABC, abstractmethod
from os import system
from typing import Optional
from PodSixNet.Connection import ConnectionListener, connection

from entities import Board, Player


class BaseScene(ABC):
    def __init__(self, network_client: 'ConnectionListener'):
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
        print("3. Exit")
        inp = input()
        while int(inp) not in [1, 2, 3]:
            print('seng nggenah blog')
            inp = input()
        scene: BaseScene
        if inp == '1':
            scene = CreateRoomScene(self._network_client)
        elif inp == '2':
            scene = JoinRoomScene(self._network_client)
        else:
            scene = EndingScene(self._network_client)
        self._network_client.change_scene(scene)
        scene.execute_scene()

    def handle_network(self, data):
        pass


class CreateRoomScene(BaseScene):
    def __init__(self, network_client: 'ConnectionListener'):
        super().__init__(network_client)
        self.__room_id: 'Optional[str]' = None

    def execute_scene(self):
        # system('cls')
        self._network_client.Send({'action': 'createroom'})
        self._wait_network_result()

    def handle_network(self, data):
        if data['action'] == 'createroomresponse':
            self._waiting_for_response = False
            self.__room_id = data['roomid']
            print(f'Room Code: {self.__room_id}')
            self._wait_network_result()
        elif data['action'] == 'playgameinfo':
            self._waiting_for_response = False
            scene = InGameScene(self._network_client, self.__room_id)
            self._network_client.change_scene(scene)
            scene.execute_scene(data)


class JoinRoomScene(BaseScene):
    def __init__(self, network_client: 'ConnectionListener'):
        super().__init__(network_client)
        self.__room_id: 'Optional[str]' = None

    def __request_room_id(self):
        self.__room_id = input("Enter room code: ")
        self._network_client.Send(
            {'action': 'joinroom', 'room_id': self.__room_id})
        self._wait_network_result()

    def execute_scene(self):
        # system('cls')
        self.__request_room_id()

    def handle_network(self, data):
        if data['action'] == 'joinroomerror':
            # system('cls')
            print(data['message'])
            self.__request_room_id()
        elif data['action'] == 'playgameinfo':
            self._waiting_for_response = False
            scene = InGameScene(self._network_client, self.__room_id)
            self._network_client.change_scene(scene)
            scene.execute_scene(data)


class InGameScene(BaseScene):
    def __init__(self, network_client: 'ConnectionListener', room_id: 'str'):
        super().__init__(network_client)
        self.__board: 'Optional[Board]' = None
        self.__current_turn: 'str' = None
        self.__player: 'Optional[Player]' = None
        self.__room_id: 'str' = room_id

    def execute_scene(self, data):
        # system('cls')
        self.handle_network(data)

    def handle_network(self, data):
        # print(data)
        if data['action'] == 'playgameinfo':
            self._waiting_for_response = False
            system('cls')
            player = Player(data['player_id'], 'player')
            opponent = Player(data['opponent_id'], 'opponent')
            self.__current_turn = data['current_turn_player_id']
            self.__board = Board([player, opponent])
            self.__player = player
            self.__handle_roll_dice()
        elif data['action'] == 'diceresult':
            self._waiting_for_response = False
            dice_result = int(data['data'])
            current_player = self.__board.getPlayer(self.__current_turn)
            move_status = self.__board.movePlayer(current_player, dice_result)
            self.__current_turn = data['current_turn_player_id']
            print(f'{current_player.get_name()} dapat dadu {str(dice_result)}')
            if move_status == 1: print(f'Ouh, {current_player.get_name()} got snake\n')
            elif move_status == 2: print(f'Wow, {current_player.get_name()} got ladder\n')
            self.__handle_roll_dice()

    def __handle_roll_dice(self):
        players = self.__board.getPlayers()
        for player in players:
            print(
                f'{player.get_name()} position: {self.__board.getPlayerPosition(player.get_id())}')
        print()
        if self.__player.get_id() == self.__current_turn:
            input("Your turn, press enter to roll dice")
            self._network_client.Send(
                {'action': 'rolldice', 'room_id': self.__room_id})
            self._wait_network_result()
        else:
            print("Waiting for opponent turn")
            self._wait_network_result()


class EndingScene(BaseScene):
    def __init__(self, network_client: 'ConnectionListener'):
        super().__init__(network_client)

    def execute_scene(self):
        print("Terimakasih telah memainkan game kami :-)")

    def handle_network(self, data):
        pass
