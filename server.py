import logging, argparse, atexit, random, string
import socket
import threading
from protocol import Action, Status
import protocol

def cleanup(server):
	server.close()
	logger.info("Server stopped.")

def init_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Game Server")
	parser.add_argument("--debug", help="Debug mode", action="store_true")
	parser.add_argument("-p", "--port", type=int, default=protocol.PORT, help="Port number")
	parser.add_argument("-m", "--max-connections", type=int, default=4, help="Maximum number of connections")
	args = parser.parse_args()
	return args

def init_logger(args) -> logging.Logger:
	global logger
	logger = logging.getLogger("Server")

	if args.debug:
		logger.setLevel(logging.DEBUG)
	else:
		logger.setLevel(logging.INFO)

	file_handler = logging.FileHandler("server.log", mode='w', encoding="utf-8")
	console_handler = logging.StreamHandler()

	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	file_handler.setFormatter(formatter)
	console_handler.setFormatter(formatter)
	
	logger.addHandler(file_handler)
	logger.addHandler(console_handler)

class LobbyManager:
	def __init__(self):
		self.lobbies = []

	def generate_lobby_code(self, key_len=4, tries=0):
		if tries >= 3:
			key_len += 1
		code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
		if code in [lobby["code"] for lobby in self.lobbies]:
			return self.generate_lobby_code(key_len, tries + 1)
		return code
	
	def create_lobby(self, client_socket):
		logger.info("Creating lobby...")
		lobby_code = self.generate_lobby_code()
		lobby = {
			"code": lobby_code,
			"host": client_socket,
			"clients": [],
			"game": None,
		}
		self.lobbies.append(lobby)
		client_socket.sendall(protocol.pack(Action.CREATE_LOBBY, lobby_code))
	
	def join_lobby(self, client_socket, code):
		lobby = next((lobby for lobby in self.lobbies if lobby["code"] == code), None)
		if lobby:
			
			if client_socket in lobby["clients"]:
				client_socket.sendall(protocol.pack(Action.JOIN_LOBBY, Status.OK))
				return
			
			lobby["clients"].append(client_socket)
			logger.info(f"Added client to lobby {code} ({len(lobby['clients'])}/2)")
			client_socket.sendall(protocol.pack(Action.JOIN_LOBBY, Status.OK))
					
			if len(lobby["clients"]) == 2:
				logger.info(f"Starting game in lobby {code}...")
				for client in lobby["clients"]:
					client.sendall(protocol.pack(Action.START_GAME, Status.OK))
		else:
			client_socket.sendall(protocol.pack(Action.JOIN_LOBBY, Status.NOT_FOUND)) 
				   
	def start_game(self, lobby):
		logger.info(f"Starting game in lobby {lobby['code']}...")
		lobby["game"] = True
		for client in lobby["clients"]:
			client.sendall(protocol.pack(Action.START_GAME, Status.OK))

	def get_lobbies(self):
		lobbies = [lobby["code"] for lobby in self.lobbies]
		return "\n".join(lobbies)

class GameServer:
	def __init__(self, max_connections: int = 4, port: int = protocol.PORT):
		self.address = "0.0.0.0"
		self.port = port
		self.max_connections = max_connections

		try:
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error as e:
			logger.critical(f"Error creating socket: {e}")
			return
		
		try:
			self.server.bind((self.address, self.port))
		except socket.error as e:
			logger.critical(f"Error binding socket: {e}")
			return
		
		try:
			self.server.listen(self.max_connections)
		except socket.error as e:
			logger.critical(f"Error listening on socket: {e}")
			return
		
		logger.info(f"Server listening on {self.address}:{self.port}")

		self.clients = []
		self.lobby_manager = LobbyManager()
		self.start()

	def start(self):
		threading.Thread(target=self.server_console).start()
		while True:
			client_socket, client_addr = self.server.accept()
			logger.info(f"Connection from: {client_addr}")
			client = (client_socket, client_addr)
			self.clients.append(client)
			threading.Thread(target=self.handle_client, args=(client,)).start()
	
	def handle_client_request(self, client_socket, action, args):
		logger.debug(f"Handling request: action={action} args={args} from {client_socket.getpeername()}")
		match action:
			case Action.CREATE_LOBBY:
				self.lobby_manager.create_lobby(client_socket)
			case Action.LOBBY_LIST:
				client_socket.sendall(protocol.pack(Action.LOBBY_LIST,
					 self.lobby_manager.get_lobbies()))
			case Action.JOIN_LOBBY:
				self.lobby_manager.join_lobby(client_socket, args)
			case _:
				logger.warning(f"Unknown action: {action}")

	def handle_client(self, client):
		client_socket, client_addr = client

		logger.info(f"Client {client_addr} connected.")
		while True:
			try:
				action, args = protocol.unpack(client_socket)
			except socket.error as e:
				logger.error(f"Error receiving data from {client_addr}: {e}")
				break

			self.handle_client_request(client[0], action, args)

		# Handle disconnection
		logger.info(f"Connection closed: {client_addr}")
		client_socket.close()
		self.clients.remove(client)

	def server_console(self):
		while True:
			command = input("Server > ")
			match command:
				case "exit":
					self.close()
					break
				case "list":
					print("Connected clients:")
					for client in self.clients:
						print(client[1])
				case "lobbies":
					print("Active lobbies:")
					for lobby in self.lobby_manager.lobbies:
						print(lobby["code"])
				case _:
					print("Invalid command.")

	def close(self):
		self.server.close()

def main() -> None:
	args = init_args()
	init_logger(args)

	logger.debug(f"Arguments: {args}")

	server = GameServer()
	atexit.register(cleanup, server)


if __name__ == "__main__":
	main()