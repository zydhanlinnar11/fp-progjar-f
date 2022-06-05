from PodSixNet.Connection import ConnectionListener, connection
import pygame
from pygame.locals import *

SERVER_HOST: "str" = "localhost"
SERVER_PORT: "int" = 5071


class GameClient(ConnectionListener):

    def __init__(self, host: "str", port: "int"):
        self.Connect((host, port))
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400

    def Network(self, data):
        print(data)
        self.Send({"action": "move"})

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def __handle_game_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def __handle_game_loop(self):
        pass

    def __handle_render(self):
        pass

    def __handle_cleanup(self):
        pygame.quit()

    def run_game(self):
        if self.on_init() == False:
            self._running = False

        while(self._running):
            for event in pygame.event.get():
                self.__handle_game_event(event)
            self.__handle_game_loop()
            self.__handle_render()
        self.__handle_cleanup()


if __name__ == '__main__':
    client = GameClient(SERVER_HOST, SERVER_PORT)
    while 1:
        client.run_game()
        connection.Pump()
        client.Pump()
