from time import sleep
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

SERVER_HOST: "str" = "localhost"
SERVER_PORT: "int" = 5071


class ClientChannel(Channel):
    def Network(self, data):
        print(data)


class GameServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)

    def Connected(self, channel, addr):
        print("new connection:", channel)


if __name__ == '__main__':
    server = GameServer(localaddr=(SERVER_HOST, SERVER_PORT))

    while True:
        server.Pump()
        sleep(0.0001)
