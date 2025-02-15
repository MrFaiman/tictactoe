import socket
import threading
from protocol import Action, Status
import protocol

class ClientState:
    CONNECTED = 1
    LOBBY = 2
    GAME = 3

class GameClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print(f"Error creating socket: {e}")
            return
        
        self.connect()
        
    def connect(self):
        try:
            self.client.connect((self.host, self.port))
        except socket.error as e:
            print(f"Error connecting to server: {e}")
            return
        
        print(f"Connected to {self.host}:{self.port}")
        
        self.get_lobbies()
        self.state = ClientState.CONNECTED

    def get_lobbies(self):
        print("Getting lobbies...")
        self.client.sendall(protocol.pack(Action.LOBBY_LIST))
        action, resp = protocol.unpack(self.client)
        if action == Action.LOBBY_LIST:
            print(resp)
        else:
            print("Unexpected response.")

    def create_lobby(self):
        print("Creating lobby...")
        self.client.sendall(protocol.pack(Action.CREATE_LOBBY))
        action, resp = protocol.unpack(self.client)
        if action == Action.CREATE_LOBBY:
            print(f"Lobby code: {resp}")
            self.join_lobby(resp)
        else:
            print("Unexpected response.")

    def join_lobby(self, code: str):
        print(f"Joining lobby {code}...")
        self.client.sendall(protocol.pack(Action.JOIN_LOBBY, code))
        action, resp = protocol.unpack(self.client)
        if action == Action.JOIN_LOBBY:
            self.state = ClientState.LOBBY
            print(resp)
            threading.Thread(target=self.wait_for_start_game).start()
        else:
            print("Unexpected response.")

    def wait_for_start_game(self):
        print("Waiting for game to start...")
        while True:
            action, resp = protocol.unpack(self.client)
            print(action, resp)
            if action == Action.START_GAME and resp == Status.OK:
                self.state = ClientState.GAME
                print("Game started!")
                break

    def start_game(self):
        print("Starting game...")
        self.client.sendall(protocol.pack(Action.START_GAME))
        action, resp = protocol.unpack(self.client)
        if action == Action.START_GAME:
            self.state = ClientState.GAME
            print(resp)
        else:
            print("Unexpected response.")

    def disconnect(self):
        print("Disconnecting...")
        self.client.sendall(protocol.pack(Action.EXIT))
        self.client.close()

def main():
    print("Starting client...")
    client = GameClient("127.0.0.1", protocol.PORT)
    
    while True:
        command = input("TicTacToe > ")

        args = command.split(" ")
        
        match args[0]:
            case "exit":
                client.disconnect()
                break
            case "lobbies":
                client.get_lobbies()
            case "create":
                client.create_lobby()
            case "join":
                client.join_lobby(args[1])
            case _:
                print("Invalid command.")
        # client.client.recv(1024)


if __name__ == "__main__":
    main()