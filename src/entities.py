from enum import Enum
from random import randint


class Dice:
    def roll(self) -> int:
        return randint(1, 6)


class Player:
    def __init__(self, id: 'int') -> None:
        self.__id = id

    def get_id(self) -> int:
        return self.__id


class Session:
    def __init__(self, players: 'list[Player]') -> None:
        if len(players) == 0:
            raise Exception('No player specified')
        self.__player_count = len(players)
        self.__players = players
        self.__turn_index = 0

    def get_current_turn(self) -> 'Player':
        return self.__players[self.__turn_index]

    def switch_turn(self):
        self.__turn_index = (self.__turn_index + 1) % self.__player_count


class CharacterColor(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)


class Character:
    def __init__(self, player_id: 'int', color: 'CharacterColor') -> None:
        self.__player_id = player_id
        self.__color = color

    def get_player_id(self) -> 'int':
        return self.__player_id

    def get_color(self) -> 'CharacterColor':
        return self.__color


class CharacterMovementType(Enum):
    MAJU = 1
    MUNDUR = 2
    KEPLESET = 3
    NAIK_TANGGA = 4


class CharacterMovement:
    def __init__(self, type: 'CharacterMovementType', destination: 'int') -> None:
        self.__type = type
        self.__destination = destination

    def get_type(self) -> 'CharacterMovementType':
        return self.__type

    def get_destination(self) -> int:
        return self.__destination


class Board:
    def __init__(self) -> None:
        pass
