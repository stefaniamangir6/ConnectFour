from board.board_repo import Board
from board.service_board import Service_Game
from validation.validators import Move_Validator
from presentation.console import UI


if __name__ == '__main__':
    rows = 6
    columns = 7
    valid_move = Move_Validator()
    Board = Board(rows, columns)
    game_Service = Service_Game(Board, valid_move)
    cons = UI(game_Service)
    cons.run()