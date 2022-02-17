from errors.exceptions import RepoError

class Board:
    def __init__(self, rows, columns):
        self.__board = [[' ' for x in range(columns)] for y in range(rows)]
        self.__rows = rows
        self.__columns = columns

    def add(self, move):
        ''' Executes a move '''
        row = self.__rows - 1
        while self.__board[row][move.get_column()] != ' ':
            row -= 1
            if row < 0 and move.get_piece_type() == 'x':
                raise RepoError("no more moves on this column!\n")
        self.__board[row][move.get_column()] = move.get_piece_type()
        return row

    def get_board(self):
        ''' Get the game board '''
        return self.__board

