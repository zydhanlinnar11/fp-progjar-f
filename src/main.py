from PodSixNet.Connection import ConnectionListener, connection
from time import sleep

SERVER_HOST: "str" = "localhost"
SERVER_PORT: "int" = 5071


class NetworkClient(ConnectionListener):

    def __init__(self, host: "str", port: "int"):
        self.Connect((host, port))

    def Network(self, data):
        print(data)
        self.Send({"action": "move"})


if __name__ == '__main__':
    client = NetworkClient(SERVER_HOST, SERVER_PORT)
    while 1:
        connection.Pump()
        client.Pump()
