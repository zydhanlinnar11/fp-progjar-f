from enum import Enum
from random import randint


class Dice:
    def roll(self) -> int:
        return randint(1, 6)


class Player:
    def __init__(self, id: 'str', name: 'str') -> None:
        self.__id = id
        self.__name = name

    def get_id(self) -> str:
        return self.__id

    def get_name(self) -> str:
        return self.__name


class Board:
    def __init__(self, players: 'list[Player]') -> None:
        self.__players = players
        self.__size = 10
        self.__snakes = {4: 2, 8: 5}
        self.__ladders = {3: 5, 7: 9}
        self.__playerPosition = {}
        for player in players:
            self.__playerPosition[player.get_id()] = 0

    def getPlayer(self, playerId: 'str') -> Player:
        for player in self.__playerPosition:
            if player.get_id() == playerId:
                return player

    def getPlayerPosition(self, playerId: 'str') -> int:
        return self.__playerPosition.get(playerId)

    def isSnake(self, position: 'int'):
        return self.__snakes.get(position) != None

    def isLadder(self, position: 'int'):
        return self.__ladders.get(position) != None

    def movePlayer(self, player: 'Player', diceResult: 'int') -> None:
        dest = 0
        position = self.getPlayerPosition(player.get_id()) + diceResult

        if(self.isSnake(position)):
            dest = self.__snakes.get(position)
        elif(self.isLadder(position)):
            dest = self.__ladders.get(position)
        elif(position > self.__size):
            dest = 2 * self.__size - position

        self.__playerPosition[player.get_id()] = dest
