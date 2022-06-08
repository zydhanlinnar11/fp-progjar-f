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

class Character:
    def __init__(self, player_id: 'str') -> None:
        self.__player_id = player_id

    def get_player_id(self) -> 'int':
        return self.__player_id

class CharacterMovementType(Enum):
    BIASA = 1
    KEPLESET = 2
    NAIK_TANGGA = 3

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
