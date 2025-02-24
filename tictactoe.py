class TicTacToe:
    numbers: list[str] = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']
    box_chars: dict[str, str] = {
        'horizontal': '━', 'vertical': '┃', 'cross': '╋',
        'top_t': '┳', 'bottom_t': '┻', 'left_t': '┣', 'right_t': '┫',
        'top_left': '┏', 'top_right': '┓', 'bottom_left': '┗', 'bottom_right': '┛'
    }

    def __init__(self) -> None:
        self.x_board: int = 0
        self.o_board: int = 0
        self.current_player: str = 'X'

    def make_move(self, position: int) -> bool:
        if not (0 <= position <= 8) or self.is_position_occupied(position):
            return False
        if self.current_player == 'X':
            self.x_board |= (1 << position)
            self.current_player = 'O'
        else:
            self.o_board |= (1 << position)
            self.current_player = 'X'
        return True

    def is_position_occupied(self, position: int) -> bool:
        return (self.x_board & (1 << position)) or (self.o_board & (1 << position))

    def get_board_state(self) -> list[str]:
        board = [' '] * 9
        for i in range(9):
            if self.x_board & (1 << i):
                board[i] = 'X'
            elif self.o_board & (1 << i):
                board[i] = 'O'
            else:
                board[i] = str(self.numbers[i+1])
        return board

    def print_board(self) -> None:
        board = self.get_board_state()
        b = self.box_chars
        h = b['horizontal'] * 3
        print(f' {b["top_left"]}{h}{b["top_t"]}{h}{b["top_t"]}{h}{b["top_right"]} ')
        print(f' {b["vertical"]} {board[0]} {b["vertical"]} {board[1]} {b["vertical"]} {board[2]} {b["vertical"]} ')
        print(f' {b["left_t"]}{h}{b["cross"]}{h}{b["cross"]}{h}{b["right_t"]} ')
        print(f' {b["vertical"]} {board[3]} {b["vertical"]} {board[4]} {b["vertical"]} {board[5]} {b["vertical"]} ')
        print(f' {b["left_t"]}{h}{b["cross"]}{h}{b["cross"]}{h}{b["right_t"]} ')
        print(f' {b["vertical"]} {board[6]} {b["vertical"]} {board[7]} {b["vertical"]} {board[8]} {b["vertical"]} ')
        print(f' {b["bottom_left"]}{h}{b["bottom_t"]}{h}{b["bottom_t"]}{h}{b["bottom_right"]} ')

    def check_winner(self) -> str | None:
        winning_combinations = [
            0b111000000, 0b000111000, 0b000000111,
            0b100100100, 0b010010010, 0b001001001,
            0b100010001, 0b001010100
        ]
        for combination in winning_combinations:
            if (self.x_board & combination) == combination:
                return 'X'
            if (self.o_board & combination) == combination:
                return 'O'
        if self.is_board_full():
            return 'Draw'
        return None

    def is_board_full(self) -> bool:
        return ((self.x_board | self.o_board) & 0b111111111) == 0b111111111

    def reset(self) -> None:
        self.x_board = 0
        self.o_board = 0
        self.current_player = 'X'