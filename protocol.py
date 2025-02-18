from socket import socket
import struct

PORT = 12345

LENGTH_FIELD_SIZE = 4
ACTION_FIELD_SIZE = 1

class Status:
	OK = "OK"
	ERROR = "ERROR"
	NOT_FOUND = "NOT_FOUND"

class Action:
	CONNECT = 1
	DISCONNECT = 2
	LOBBY_LIST = 3
	CREATE_LOBBY = 4
	JOIN_LOBBY = 5
	START_GAME = 6

def unpack(sock: socket):
	# Receive the action (1 byte)
	action_data = sock.recv(ACTION_FIELD_SIZE)
	if not action_data:
		return -1, ""
	action = struct.unpack('!B', action_data)[0]
	
	# Receive the length of the args (4 bytes)
	length_data = sock.recv(LENGTH_FIELD_SIZE)
	if not length_data:
		return -1, ""
	data_len = struct.unpack('!I', length_data)[0]
	
	# Receive the args
	if data_len == 0:
		return action, ""
	arg = sock.recv(data_len).decode()
	
	return action, arg

def pack(action: int = 0, arg: str = "") -> bytes:
	# Pack the action (1 byte)
	action_data = struct.pack('!B', action)
	
	# Pack the length of the args (4 bytes)
	arg = str(arg)
	data_len = len(arg)
	length_data = struct.pack('!I', data_len)
	
	# Pack the args
	arg_data = arg.encode()
	
	# Combine all parts
	packet = action_data + length_data + arg_data
	return packet