import socket
from protocol import Protocol, Actions
from tictactoe import TicTacToe

class Client:
    def __init__(self, host: str, port: int, player_symbol: str) -> None:
        self.sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_host(host, port)
        self.game: TicTacToe = TicTacToe()
        self.player_symbol: str = player_symbol

    def connect_to_host(self, host: str, port: int) -> None:
        while True:
            try:
                self.sock.connect((host, port))
                break
            except (socket.error, socket.gaierror) as e:
                print(f"Error connecting to host: {e}")
                host = input("Enter a valid host IP: ")
                port = int(input("Enter a valid host port: "))

    def send(self, action: int, argument: int) -> None:
        message = Protocol.pack(action, argument)
        self.sock.sendall(message)

    def receive(self) -> tuple[int, int]:
        return Protocol.unpack(self.sock)

    def play(self) -> None:
        while True:
            self.game.print_board()
            if self.game.current_player == self.player_symbol:
                position = int(input(f"Your move ({self.player_symbol}) (1-9): ")) - 1
                if self.game.make_move(position):
                    self.send(Actions.MOVE, position)
                else:
                    print("Invalid move. Try again.")
            else:
                print(f"Waiting for opponent's move ({'O' if self.player_symbol == 'X' else 'X'})...")
                try:
                    action, position = self.receive()
                    if action == Actions.MOVE:
                        self.game.make_move(position)
                except ValueError as e:
                    print(f"Error: {e}")
                    continue
            winner = self.game.check_winner()
            if winner:
                self.game.print_board()
                if winner == 'Draw':
                    print("It's a draw!")
                else:
                    print(f"{winner} wins!")
                break

        self.ask_play_again()

    def ask_play_again(self) -> None:
        play_again = input("Do you want to play again? (y/n): ").lower() == 'y'
        self.send(Actions.PLAY_AGAIN, int(play_again))
        if play_again:
            print("Waiting for opponent's decision...")
            action, response = self.receive()
            if action == Actions.PLAY_AGAIN and response == 1:
                print("Opponent agreed to play again!")
                self.game.reset()
                self.play()
            else:
                print("Opponent declined to play again.")
        else:
            print("You declined to play again.")

class Host(Client):
    def __init__(self, port: int) -> None:
        self.sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_to_port(port)
        self.sock.listen(1)
        print("Waiting for a connection...")
        self.connection, _ = self.sock.accept()
        print("Opponent connected!")
        self.game: TicTacToe = TicTacToe()
        self.player_symbol: str = 'X'  # Host always starts as 'X'

    def bind_to_port(self, port: int) -> None:
        while True:
            try:
                self.sock.bind(('0.0.0.0', port))
                break
            except socket.error as e:
                print(f"Error binding to port: {e}")
                port = int(input("Enter a different port to host on: "))

    def send(self, action: int, argument: int) -> None:
        message = Protocol.pack(action, argument)
        self.connection.sendall(message)

    def receive(self) -> tuple[int, int]:
        return Protocol.unpack(self.connection)