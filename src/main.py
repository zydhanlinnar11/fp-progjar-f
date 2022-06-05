from PodSixNet.Connection import ConnectionListener, connection
import pygame
from pygame.locals import *
from scenes import MainMenuScene, BaseScene

SERVER_HOST: "str" = "localhost"
SERVER_PORT: "int" = 5071


class GameClient(ConnectionListener):

    def __init__(self, host: "str", port: "int"):
        pygame.init()
        self.Connect((host, port))
        self.size = self.weight, self.height = 640, 400
        self._running = True
        self._display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.__scene: 'BaseScene.BaseScene' = MainMenuScene.MainMenuScene(
            display_surface=self._display_surf)

    def Network(self, data):
        print(data)
        self.Send({"action": "move"})

    def __handle_cleanup(self):
        pygame.quit()

    def run_game(self):
        while(self._running):
            connection.Pump()
            self.Pump()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self._running = False
            self.__scene.handle_game_event(events)
            self.__scene.handle_game_loop()
            self.__scene.handle_game_render()
            self.__scene = self.__scene.get_next_scene()
        self.__handle_cleanup()


if __name__ == '__main__':
    client = GameClient(SERVER_HOST, SERVER_PORT)
    client.run_game()
