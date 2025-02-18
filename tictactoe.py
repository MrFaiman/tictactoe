class TicTacToe:
	numbers = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']
	box_chars = {
		'horizontal': '━',    # horizontal line
		'vertical': '┃',      # vertical line
		'cross': '╋',         # cross intersection
		'top_t': '┳',         # T-piece pointing down
		'bottom_t': '┻',      # T-piece pointing up
		'left_t': '┣',        # T-piece pointing right
		'right_t': '┫',       # T-piece pointing left
		'top_left': '┏',      # top-left corner
		'top_right': '┓',     # top-right corner
		'bottom_left': '┗',   # bottom-left corner
		'bottom_right': '┛'   # bottom-right corner
	}
	def __init__(self):
		# Initialize two integers to represent X's and O's positions
		self.x_board = 0  # positions of X
		self.o_board = 0  # positions of O
		self.current_player = 'X'

	def make_move(self, position):
		"""
		Make a move at the given position (0-8)
		Returns True if move is valid, False otherwise
		"""
		if not (0 <= position <= 8):
			return False

		# Check if position is already occupied
		if self.is_position_occupied(position):
			return False

		# Set the bit at the given position
		if self.current_player == 'X':
			self.x_board |= (1 << position)
			self.current_player = 'O'
		else:
			self.o_board |= (1 << position)
			self.current_player = 'X'
		
		return True

	def is_position_occupied(self, position):
		"""Check if a position is already occupied"""
		return (self.x_board & (1 << position)) or (self.o_board & (1 << position))

	def get_board_state(self):
		"""Returns the current board state as a list"""
		board = [' '] * 9
		for i in range(9):
			if self.x_board & (1 << i):
				board[i] = 'X'
			elif self.o_board & (1 << i):
				board[i] = 'O'
			else:
				board[i] = str(self.numbers[i+1])
		return board

	def print_board(self):
		"""Print the board using the selected box drawing style"""
		board = self.get_board_state()
		b = self.box_chars  # shorthand reference to box characters
		h = b['horizontal'] * 3  # three horizontal lines

		print(f' {b["top_left"]}{h}{b["top_t"]}{h}{b["top_t"]}{h}{b["top_right"]} ')
		print(f' {b["vertical"]} {board[0]} {b["vertical"]} {board[1]} {b["vertical"]} {board[2]} {b["vertical"]} ')
		print(f' {b["left_t"]}{h}{b["cross"]}{h}{b["cross"]}{h}{b["right_t"]} ')
		print(f' {b["vertical"]} {board[3]} {b["vertical"]} {board[4]} {b["vertical"]} {board[5]} {b["vertical"]} ')
		print(f' {b["left_t"]}{h}{b["cross"]}{h}{b["cross"]}{h}{b["right_t"]} ')
		print(f' {b["vertical"]} {board[6]} {b["vertical"]} {board[7]} {b["vertical"]} {board[8]} {b["vertical"]} ')
		print(f' {b["bottom_left"]}{h}{b["bottom_t"]}{h}{b["bottom_t"]}{h}{b["bottom_right"]} ')

	def check_winner(self):
		"""
		Check if there's a winner
		Returns 'X' or 'O' if there's a winner, 'Draw' if game is drawn, None if game is still ongoing
		"""
		# Winning combinations in binary
		winning_combinations = [
			0b111000000,  # top row
			0b000111000,  # middle row
			0b000000111,  # bottom row
			0b100100100,  # left column
			0b010010010,  # middle column
			0b001001001,  # right column
			0b100010001,  # diagonal
			0b001010100   # other diagonal
		]

		# Check for winner
		for combination in winning_combinations:
			if (self.x_board & combination) == combination:
				return 'X'
			if (self.o_board & combination) == combination:
				return 'O'

		# Check for draw
		if self.is_board_full():
			return 'Draw'

		return None

	def is_board_full(self):
		"""Check if the board is full"""
		return ((self.x_board | self.o_board) & 0b111111111) == 0b111111111
		


def main():
	tictactoe = TicTacToe()
	while True:
		tictactoe.print_board()
		position = int(input(f"{tictactoe.current_player}'s turn: "))
		if not tictactoe.make_move(position-1):
			print("Invalid move. Try again.")
			continue

		winner = tictactoe.check_winner()
		if winner:
			tictactoe.print_board()
			if winner == 'Draw':
				print("It's a draw!")
			else:
				print(f"{winner} wins!")
			break

if __name__ == "__main__":
	main()
