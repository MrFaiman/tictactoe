# TicTacToe Multiplayer Game

This project is a multiplayer TicTacToe game implemented in Python. It allows two players to play against each other over a network using a command-line interface (CLI). Players can choose to host a game or join an existing game.

## Key Features

- **Multiplayer Support**: Play TicTacToe with another player over a network.
- **Command-Line Interface**: Simple and straightforward CLI for gameplay.
- **Network Communication**: Uses sockets for client-server communication.
- **Play Again Option**: After a game ends, players can choose to play another round.
- **Error Handling**: Handles common network errors, such as invalid host or port.

## Example I/O

### Host

- **Input**:
  ```plaintext
  Do you want to host (h) or join (j) a game? h
  Enter port to host on: 12345
  ```

- **Output**:
  ```plaintext
  Waiting for a connection...
  Opponent connected!
  ```

### Join

- **Input**:
  ```plaintext
  Do you want to host (h) or join (j) a game? j
  Enter host IP: 192.168.1.2
  Enter host port: 12345
  ```

- **Output**:
  ```plaintext
  Waiting for opponent's move...
  ```

### Gamplay
```
 ┏━━━┳━━━┳━━━┓ 
 ┃ X ┃ 2 ┃ 3 ┃ 
 ┣━━━╋━━━╋━━━┫ 
 ┃ 4 ┃ 5 ┃ 6 ┃ 
 ┣━━━╋━━━╋━━━┫ 
 ┃ 7 ┃ 8 ┃ 9 ┃ 
 ┗━━━┻━━━┻━━━┛ 
O's turn: 5
 ┏━━━┳━━━┳━━━┓ 
 ┃ X ┃ 2 ┃ 3 ┃ 
 ┣━━━╋━━━╋━━━┫ 
 ┃ 4 ┃ O ┃ 6 ┃ 
 ┣━━━╋━━━╋━━━┫ 
 ┃ 7 ┃ 8 ┃ 9 ┃ 
 ┗━━━┻━━━┻━━━┛ 
```

## File List and Contents
`protocol.py`: Contains the Actions and Protocol classes for defining game actions and handling message packing/unpacking.

`tictactoe.py`: Contains the TicTacToe class, which manages the game state, checks for valid moves, and determines the winner.

`client.py`: Contains the Client and Host classes for handling network communication and game logic for both hosting and joining a game.

`main.py`: Entry point for the CLI version of the game. Prompts the user to host or join a game and starts the CLI game loop.