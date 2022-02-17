import unittest
from domain.entity_move import Move
from validation.validators import Move_Validator
from errors.exceptions import ValidationError, RepoError
from board.board_repo import Board
from board.service_board import Service_Game

class Move_Entity_Test(unittest.TestCase):

    def setUp(self):
        self.__move = Move(3, 'x')

    def test_create_move(self):
        assert(self.__move.get_column() == 3)
        assert(self.__move.get_piece_type() == 'x')

    def test_set_piece_type(self):
        self.__move.set_piece_type('o')
        assert (self.__move.get_piece_type() == 'o')

class Validator_Test(unittest.TestCase):

    def test_valid(self):
        bad_move = Move(10, "")
        move_valid = Move_Validator()
        try:
            move_valid.validate(bad_move)
            assert(False)
        except ValidationError as ve:
            assert (str(ve) == "invalid column!\ninvalid name!\n")

        bad_move = Move(-8, "o")
        move_valid = Move_Validator()
        try:
            move_valid.validate(bad_move)
            assert (False)
        except ValidationError as ve:
            assert (str(ve) == "invalid column!\ninvalid name!\n")

class Test_Board(unittest.TestCase):

    def setUp(self):
        self.__board = Board(6,7)

    def test_add(self):
        move = Move(5, 'x')
        self.__board.add(move)
        copy_board = self.__board.get_board()
        assert(copy_board[5][5] == 'x')
        self.__board.add(move)
        self.__board.add(move)
        self.__board.add(move)
        self.__board.add(move)
        self.__board.add(move)
        try:
            self.__board.add(move)
            assert(False)
        except RepoError as re:
            assert(str(re) == "no more moves on this column!\n")

class Test_Service_board(unittest.TestCase):

    def setUp(self):
        self.__board = Board(6, 7)
        self.__valid = Move_Validator()
        self.__Board_Service = Service_Game(self.__board, self.__valid)

    def test_add_player_move(self):
        row = self.__Board_Service.add_player_move(5,'x')
        copy_board = self.__board.get_board()
        assert (copy_board[5][5] == 'x')
        assert(row == 5)

    def test_play_game_1(self):
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(1, 'x')
        self.__board.add(move)
        move = Move(2, 'x')
        row = self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 2)
        self.__Board_Service.add_computer_player_move(row, 2)
        copy_board = self.__board.get_board()
        assert (copy_board[5][3] == 'o')


    def test_play_game_2(self):
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(3, 'x')
        self.__board.add(move)
        move = Move(4, 'x')
        row = self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 4)
        copy_board = self.__board.get_board()
        assert (copy_board[5][1] == 'o')

    def test_play_game_3(self):
        move = Move(1, 'x')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(4, 'x')
        row = self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 4)
        copy_board = self.__board.get_board()
        assert (copy_board[5][3] == 'o')

    def test_play_game_4(self):
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(3, 'x')
        row = self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 3)
        copy_board = self.__board.get_board()
        assert (copy_board[5][1] == 'o')

    def test_play_game_5(self):
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(2, 'x')
        row = self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 2)
        copy_board = self.__board.get_board()
        assert (copy_board[2][2] == 'o')

    def test_play_game_6(self):
        move = Move(2, 'o')
        self.__board.add(move)
        move = Move(2, 'o')
        self.__board.add(move)
        move = Move(2, 'o')
        self.__board.add(move)
        move = Move(2, 'x')
        row = self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 2)
        copy_board = self.__board.get_board()
        assert (copy_board[1][2] == ' ')

    def test_add_random(self):
        self.__Board_Service._add_random()

    def test_play_game_7(self):
        move = Move(2, 'o')
        row = self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(3, 'x')
        self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 2)
        copy_board = self.__board.get_board()
        assert (copy_board[5][1] == 'o')

    def test_play_game_8(self):
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'x')
        row = self.__board.add(move)
        move = Move(2, 'o')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(3, 'x')
        self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 1)
        copy_board = self.__board.get_board()
        assert (copy_board[2][0] == 'o')

    def test_play_game_9(self):
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'x')
        row = self.__board.add(move)
        move = Move(2, 'o')
        self.__board.add(move)
        move = Move(3, 'x')
        self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 1)
        copy_board = self.__board.get_board()
        assert (copy_board[4][2] == 'o')

    def test_play_game_10(self):
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'x')
        row = self.__board.add(move)
        move = Move(2, 'o')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 1)
        copy_board = self.__board.get_board()
        assert (copy_board[5][3] == 'o')

    def test_play_game_11(self):
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'x')
        row = self.__board.add(move)
        move = Move(2, 'o')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 1)
        res = self.__Board_Service.check_win()
        assert(res == None)

    def test_play_game_12(self):
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'x')
        row = self.__board.add(move)
        move = Move(2, 'o')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(4, 'o')
        self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 1)
        res = self.__Board_Service.check_win()
        assert(res == 'o')

    def test_play_game_13(self):
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'x')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'x')
        row = self.__board.add(move)
        move = Move(4, 'o')
        self.__board.add(move)
        move = Move(4, 'x')
        self.__board.add(move)
        move = Move(3, 'x')
        self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 5)
        copy_board = self.__board.get_board()
        assert(copy_board[2][6] =='o')

    def test_play_game_14(self):
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'x')
        self.__board.add(move)
        move = Move(6, 'x')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'x')
        row = self.__board.add(move)
        move = Move(4, 'o')
        self.__board.add(move)
        move = Move(3, 'x')
        self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 5)
        copy_board = self.__board.get_board()
        assert(copy_board[4][4] =='o')

    def test_play_game_15(self):
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'x')
        self.__board.add(move)
        move = Move(6, 'x')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'x')
        row = self.__board.add(move)
        move = Move(4, 'x')
        self.__board.add(move)
        move = Move(4, 'x')
        self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 5)
        copy_board = self.__board.get_board()
        assert (copy_board[5][3] == 'o')

    def test_play_game_16(self):
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(0, 'x')
        row = self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'x')
        self.__board.add(move)
        move = Move(2, 'o')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(3, 'x')
        self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 0)
        copy_board = self.__board.get_board()
        assert (copy_board[3][1] == 'o')

    def test_play_game_17(self):
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(0, 'x')
        row = self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'x')
        self.__board.add(move)
        move = Move(1, 'x')
        self.__board.add(move)
        move = Move(2, 'o')
        self.__board.add(move)
        move = Move(3, 'x')
        self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 0)
        copy_board = self.__board.get_board()
        assert (copy_board[4][2] == 'o')

    def test_play_game_18(self):
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(0, 'x')
        row = self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'x')
        self.__board.add(move)
        move = Move(1, 'x')
        self.__board.add(move)
        move = Move(2, 'o')
        self.__board.add(move)
        move = Move(2, '0')
        self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 0)
        copy_board = self.__board.get_board()
        assert (copy_board[5][3] == 'o')

    def test_play_game_19(self):
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'x')
        self.__board.add(move)
        move = Move(6, 'x')
        row = self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'x')
        self.__board.add(move)
        move = Move(4, 'x')
        self.__board.add(move)
        move = Move(3, 'x')
        self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 6)
        copy_board = self.__board.get_board()
        assert (copy_board[4][4] == 'o')

    def test_play_game_20(self):
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'x')
        self.__board.add(move)
        move = Move(6, 'x')
        row = self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(4, 'x')
        self.__board.add(move)
        move = Move(4, 'x')
        self.__board.add(move)
        move = Move(3, 'x')
        self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 6)
        copy_board = self.__board.get_board()
        assert (copy_board[3][5] == 'o')

    def test_play_game_21(self):
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'x')
        self.__board.add(move)
        move = Move(6, 'x')
        row = self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'x')
        self.__board.add(move)
        move = Move(4, 'x')
        self.__board.add(move)
        move = Move(4, 'x')
        self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 6)
        copy_board = self.__board.get_board()
        assert (copy_board[5][3] == 'o')

    def test_play_game_22(self):
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'x')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'x')
        self.__board.add(move)
        move = Move(4, 'x')
        self.__board.add(move)
        move = Move(4, 'x')
        row = self.__board.add(move)
        move = Move(3, 'x')
        self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 4)
        copy_board = self.__board.get_board()
        assert (copy_board[2][6] == 'o')

    def test_play_game_23(self):
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'x')
        self.__board.add(move)
        move = Move(6, 'x')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(4, 'x')
        self.__board.add(move)
        move = Move(4, 'x')
        row = self.__board.add(move)
        move = Move(3, 'x')
        self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 4)
        copy_board = self.__board.get_board()
        assert (copy_board[3][5] == 'o')

    def test_play_game_24(self):
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'x')
        self.__board.add(move)
        move = Move(6, 'x')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'x')
        self.__board.add(move)
        move = Move(4, 'x')
        self.__board.add(move)
        move = Move(4, 'x')
        row = self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 4)
        copy_board = self.__board.get_board()
        assert (copy_board[5][3] == 'o')

    def test_play_game_25(self):
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'x')
        self.__board.add(move)
        move = Move(6, 'x')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(4, 'x')
        self.__board.add(move)
        move = Move(4, 'x')
        self.__board.add(move)
        move = Move(3, 'x')
        row = self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 3)
        copy_board = self.__board.get_board()
        assert (copy_board[3][5] == 'o')

    def test_play_game_26(self):
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'x')
        self.__board.add(move)
        move = Move(6, 'x')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'x')
        self.__board.add(move)
        move = Move(4, 'x')
        self.__board.add(move)
        move = Move(3, 'x')
        row = self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 3)
        copy_board = self.__board.get_board()
        assert (copy_board[4][4] == 'o')

    def test_play_game_27(self):
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'o')
        self.__board.add(move)
        move = Move(6, 'x')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'o')
        self.__board.add(move)
        move = Move(5, 'x')
        self.__board.add(move)
        move = Move(4, 'x')
        self.__board.add(move)
        move = Move(4, 'x')
        self.__board.add(move)
        move = Move(3, 'x')
        row = self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 3)
        copy_board = self.__board.get_board()
        assert (copy_board[2][6] == 'o')

    def test_play_game_28(self):
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(2, 'x')
        row = self.__board.add(move)
        move = Move(3, 'x')
        self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 2)
        copy_board = self.__board.get_board()
        assert (copy_board[3][1] == 'o')

    def test_play_game_29(self):
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'x')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(2, 'x')
        row = self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 2)
        copy_board = self.__board.get_board()
        assert (copy_board[5][3] == 'o')

    def test_play_game_30(self):
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'x')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(2, 'x')
        row = self.__board.add(move)
        move = Move(3, 'x')
        self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 2)
        copy_board = self.__board.get_board()
        assert (copy_board[2][0] == 'o')

    def test_play_game_31(self):
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'x')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(3, 'x')
        row = self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 3)
        copy_board = self.__board.get_board()
        assert (copy_board[2][0] == 'o')

    def test_play_game_32(self):
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(3, 'x')
        row = self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 3)
        copy_board = self.__board.get_board()
        assert (copy_board[3][1] == 'o')

    def test_play_game_33(self):
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'x')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(3, 'x')
        row = self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 3)
        copy_board = self.__board.get_board()
        assert (copy_board[4][2] == 'o')

    def test_play_game_34(self):
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(3, 'x')
        row = self.__board.add(move)
        self.__Board_Service.add_computer_player_move(row, 3)
        copy_board = self.__board.get_board()
        assert (copy_board[3][1] == 'o')

    def test_play_game_35(self):
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'o')
        self.__board.add(move)
        res = self.__Board_Service.check_win()
        assert (res == 'o')

    def test_play_game_36(self):
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'o')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(0, 'x')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'o')
        self.__board.add(move)
        move = Move(1, 'x')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        move = Move(3, 'x')
        self.__board.add(move)
        move = Move(2, 'x')
        self.__board.add(move)
        res = self.__Board_Service.check_win()
        assert (res == 'x')