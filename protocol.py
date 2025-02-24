import socket

class Actions:
    MOVE: int = 1
    PLAY_AGAIN: int = 2
    VALID_ACTIONS: set[int] = {MOVE, PLAY_AGAIN}
    
class Protocol:
    @staticmethod
    def pack(action: int, argument: int) -> bytes:
        """Pack the action and argument into a 2-byte message."""
        return bytes([action, argument])

    @staticmethod
    def unpack(sock: socket.socket) -> tuple[int, int]:
        """Unpack a 2-byte message from the socket into action and argument."""
        data = sock.recv(2)
        if len(data) != 2:
            raise ValueError("Incomplete packet received")
        
        action, argument = data[0], data[1]
        
        if action not in Actions.VALID_ACTIONS:
            raise ValueError(f"Invalid action received: {action}")
        
        if action == Actions.MOVE and not (0 <= argument <= 8):
            raise ValueError(f"Invalid argument received: {argument}")
        
        return action, argument