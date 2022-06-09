from PodSixNet.Connection import ConnectionListener, connection
from scenes import MainMenuScene, BaseScene

SERVER_HOST: "str" = "localhost"
SERVER_PORT: "int" = 5071


class GameClient(ConnectionListener):

    def __init__(self, host: "str", port: "int"):
        self.Connect((host, port))
        self.__scene: 'BaseScene' = MainMenuScene(self)

    def Network(self, data):
        self.__scene.handle_network(data)

    def run_game(self):
        self.__scene.execute_scene()

    def change_scene(self, scene: 'BaseScene'):
        self.__scene = scene


if __name__ == '__main__':
    client = GameClient(SERVER_HOST, SERVER_PORT)
    client.run_game()
