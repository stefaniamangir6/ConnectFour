from domain.entity_move import Move
import random
import numpy


class Service_Game:
    def __init__(self, board_repository, move_validator):
        self.__board_repository = board_repository
        self.__move_validator = move_validator
        self.__first_move_col_comp = 0
        self.__first_move_row_comp = 0

    def add_player_move(self,column, piece_type):
        move = Move(column, piece_type)
        self.__move_validator.validate(move)
        return self.__board_repository.add(move)

    def _keep_positions(self, col_comp, row_comp):

        ''' the function keeps track of how the last move of the computer changes by retaining the row and the
        column of it
            every time the computer makes a move its final row and column are updated'''

        self.__first_move_col_comp = col_comp
        self.__first_move_row_comp = row_comp

    def _add_random(self):

        ''' function that adds a random move whenever a strategy or block move isn't available
        especially the first time'''

        col = random.randint(0, 6)
        move = Move(col, 'o')
        row = self.__board_repository.add(move)
        while row == None:
            col = random.randint(0, 6)
            move = Move(col, 'o')
            row = self.__board_repository.add(move)
        self._keep_positions(col, row)
        return col, row

    def __add_c_move(self, col):

        ''' function that basically adds a computer move '''

        move = Move(col, 'o')
        row = self.__board_repository.add(move)
        self._keep_positions(col, row)

    def __add_strategy_move(self,col_computer, row_computer, copy_board):
        ''' - function that builds a basic strategy for the computer player
            - the computer continues its moves by taking into consideration the coordinates of its last one
            and then placing the next one around the previous one depending on the free places

            |0|1|2|3|4|5|6|
            | | | | | | | |
            | | | | | | | |     the moves are placed on one of the "_" spaces; it basically tries to form a "four"
            | | | | | | | |                                                         whenever possible
            | | | |_| | | |
            | | |_|o|_| | |

             '''
        if row_computer != 0:
            if copy_board[row_computer-1][col_computer] == ' ':
                self.__add_c_move(col_computer)
                return
        if col_computer != 6:
            if copy_board[row_computer][col_computer+1] == ' ':
                self.__add_c_move(col_computer+1)
                return
        if col_computer != 0:
            if copy_board[row_computer][col_computer-1] == ' ':
                self.__add_c_move(col_computer-1)
                return
        self._add_random()


    def __case_1(self, copy_board, row, col):

        ''' the computer analyses the situation where the player has:
            ... _ ...
            ... x ...
            ... x ...
            ... x ...  and puts its move on "_" if necessary, the coordinates of the computer's last move are updated'''

        if copy_board[row][col] == copy_board[row + 1][col] == copy_board[row + 2][col]:
            self.__add_c_move(col)
            return 1
        else:
            return 0

    def __case_2(self, copy_board, row, col):
        ''' the computer analyses the situations where the player has one of :
            |0|1|2|3|4| | |     |0|1|2|3|4| | |     |0|1|2|3|4| | |     |0|1|2|3|4| | |
            | | | | | | | |     | | | | | | | |     | | | | | | | |     | | | | | | | |
            |_|_|_|_| | | |     |x|x|x|x| | | |     | |_| | | | | |     |x|x|x|x| | | |
            | |x|x|x|x| | |     | |x|x|x|x| | |     | | |x| | | | |     | |x|x|x|x| | |
            | | |x|x|x|x| |     | | |_|_|_|_| |     | |0|x|x| | | |     | | |x|x|x|x| |
            | | | |x|x|x|x|     | | | |x|x|x|x|     | |0|x| |x| | |     | | | |_|_|_|_|

            !! and _       x     x
                   (x)     (x)   (x)
                     x  or   _  or x
                      x       x     _  is the last move

        and puts its move on "_" if necessary, the coordinates of the computer's last move are updated
        moreover, if the position for the first case is empty, it doesn't put anything because it anticipates the
        player's next move and doesn't let him win '''

        if copy_board[row][col] == copy_board[row + 1][col + 1] == copy_board[row + 2][col + 2]:
            if copy_board[row][col - 1] != ' ':
                self.__add_c_move(col - 1)
                return 1
        elif copy_board[row][col] == copy_board[row -1][col - 1] == copy_board[row + 2][col + 2]:
            self.__add_c_move(col + 1)
            return 1
        elif copy_board[row][col] == copy_board[row -1][col - 1] == copy_board[row + 1][col + 1]:
            self.__add_c_move(col + 2)
            return 1
        else:
            return 0

    def __case_3(self, copy_board, row, col):
        ''' the computer analyses the situations where the player has one of :
            |0|1|2|3|4|5|6|     |0|1|2|3|4|5|6|     |0|1|2|3|4|5|6|
            | | | | | | | |     | | | | | | | |     | | | | | | | |
            | | | |_|_|_|_|     | | | |x|x|x|x|     | | | |x|x|x|x|
            | | |x|x|x|x| |     | | |x|x|x|x| |     | | |x|x|x|x| |
            | |x|x|x|x| | |     | |_|_|_|_| | |     | |x|x|x|x| | |
            |x|x|x|x| | | |     |x|x|x|x| | | |     |_|_|_|_| | | |

            !! and     _       x      x
                     (x)     (x)    (x)
                     x  or   _  or  x
                    x       x      _  is the last move

        and puts its move on "_" if necessary, the coordinates of the computer's last move are updated '''

        if copy_board[row][col] == copy_board[row + 1][col - 1] == copy_board[row + 2][col - 2]:
            if copy_board[row][col+1] != ' ':
                self.__add_c_move(col + 1)
                return 1
        elif copy_board[row][col] == copy_board[row - 1][col + 1] == copy_board[row + 2][col - 2]:
            if copy_board[row+2][col - 1] != ' ':
                self.__add_c_move(col - 1)
                return 1
        elif copy_board[row][col] == copy_board[row - 1][col + 1] == copy_board[row + 1][col - 1]:
            self.__add_c_move(col - 2)
            return 1
        else:
            return 0

    def __case_4(self, copy_board, row, col):
        ''' the computer analyses the situations where the player has:
                    |0|1|2|3|4| | |     |0|1|2|3|4| | |     |0|1|2|3|4| | |
                    | | | | | | | |     | | | | | | | |     | | | | | | | |
                    |x|x|x|x| | | |     |x|x|x|x| | | |     |x|x|x|x| | | |
                    | |_|_|_|_| | |     | |x|x|x|x| | |     | |x|x|x|x| | |
                    | | |x|x|x|x| |     | | |_|_|_|_| |     | | |x|x|x|x| |
                    | | | |x|x|x|x|     | | | |x|x|x|x|     | | | |_|_|_|_|

            !! and  (x)      (x)    (x)
                      x   or   _  or  x
                       _        x      x
                        x        x      _  is the last move

        and puts its move on "_" if necessary, the coordinates of the computer's last move are updated '''
        if copy_board[row][col] == copy_board[row + 1][col + 1] == copy_board[row + 3][col + 3]:
            self.__add_c_move(col + 2)
            return 1
        elif copy_board[row][col] == copy_board[row + 2][col + 2] == copy_board[row + 3][col + 3]:
            if copy_board[row + 2][col + 1] != ' ':
                self.__add_c_move(col + 1)
                return 1
        elif copy_board[row][col] == copy_board[row + 2][col + 2] == copy_board[row + 1][col + 1]:
            if copy_board[row +3][col + 2] != ' ':
                self.__add_c_move(col + 3)
                return 1
        else:
            return 0

    def __case_5(self, copy_board, row, col):
        ''' the computer analyses the situations where the player has:
                    |0|1|2|3|4|5|6|     |0|1|2|3|4|5|6|     |0|1|2|3|4|5|6|
                    | | | | | | | |     | | | | | | | |     | | | | | | | |
                    | | | | | | | |     | | | | | | | |     | | | | | | | |
                    | | | |x|x|x|x|     | | | |x|x|x|x|     | | | |x|x|x|x|
                    | | |x|x|x|x| |     | | |_|_|_|_| |     | | |x|x|x|x| |
                    | |_|_|_|_| | |     | |x|x|x|x| | |     | |x|x|x|x| | |
                    |x|x|x|x| | | |     |x|x|x|x| | | |     |_|_|_|_| | | |

            !! and  (x)      (x)     (x)
                    x   or   _  or  x
                   _        x      x
                  x        x      _     is the last move

        and puts its move on "_" if necessary, the coordinates of the computer's last move are updated '''
        if copy_board[row][col] == copy_board[row + 1][col - 1] == copy_board[row + 3][col - 3]:
            if copy_board[row + 3][col - 2] != ' ':
                self.__add_c_move(col - 2)
                return 1
        elif copy_board[row][col] == copy_board[row + 2][col - 2] == copy_board[row + 3][col - 3]:
            if copy_board[row+2][col - 1] != ' ':
                self.__add_c_move(col - 1)
                return 1
        elif copy_board[row][col] == copy_board[row + 1][col - 1] == copy_board[row + 2][col - 2]:
            self.__add_c_move(col - 3)
            return 1
        else:
            return 0

    def __case_6(self, copy_board, row, col):
        ''' the computer analyses the situations where the player has:
                    |0|1|2|3|4|5|6|     |0|1|2|3|4|5|6|     |0|1|2|3|4|5|6|
                    | | | | | | | |     | | | | | | | |     | | | | | | | |
                    | | | | | | | |     | | | | | | | |     | | | | | | | |
                    |_|_|_|_| | | |     |x|x|x|x| | | |     |x|x|x|x| | | |
                    | |x|x|x|x| | |     | |_|_|_|_| | |     | |x|x|x|x| | |
                    | | |x|x|x|x| |     | | |x|x|x|x| |     | | |x|x|x|x| |
                    | | | |x|x|x|x|     | | | |x|x|x|x|     | | | |_|_|_|_|

            !! and  _        x        x
                     x   or   _    or  x
                      (x)      (x)     (x)
                         x       x       _  is the last move

        and puts its move on "_" if necessary, the coordinates of the computer's last move are updated '''
        if copy_board[row][col] == copy_board[row + 1][col + 1] == copy_board[row - 1][col - 1]:
            if copy_board[row - 1][col - 2] != ' ':
                self.__add_c_move(col - 2)
                return 1
        elif copy_board[row][col] == copy_board[row + 1][col + 1] == copy_board[row - 2][col - 2]:
            if copy_board[row][col - 1] != ' ':
                self.__add_c_move(col - 1)
                return 1
        elif copy_board[row][col] == copy_board[row - 1][col - 1] == copy_board[row - 2][col - 2]:
            self.__add_c_move(col + 1)
            return 1
        else:
            return 0

    def __case_7(self, copy_board, row, col):
        ''' the computer analyses the situations where the player has:
                    |0|1|2|3|4|5|6|     |0|1|2|3|4|5|6|    |0|1|2|3|4|5|6|
                    | | | | | | | |     | | | | | | | |    | | | | | | | |
                    | | | | | | | |     | | | | | | | |    | | | | | | | |
                    | | | |_|_|_|_|     | | | |x|x|x|x|    | | | |x|x|x|x|
                    | | |x|x|x|x| |     | | |_|_|_|_| |    | | |x|x|x|x| |
                    | |x|x|x|x| | |     | |x|x|x|x| | |    | |x|x|x|x| | |
                    |x|x|x|x| | | |     |x|x|x|x| | | |    |_|_|_|_| | | |

            !! and      _        x      x
                       x   or   _  or  x
                     (x)      (x)    (x)
                    x         x      _  is the last move

        and puts its move on "_" if necessary, the coordinates of the computer's last move are updated '''
        if copy_board[row][col] == copy_board[row + 1][col - 1] == copy_board[row - 1][col + 1]:
            if copy_board[row-1][col + 2] != ' ':
                self.__add_c_move(col + 2)
                return 1
        elif copy_board[row][col] == copy_board[row + 1][col - 1] == copy_board[row - 2][col + 2]:
            if copy_board[row][col + 1] != ' ':
                self.__add_c_move(col + 1)
                return 1
        elif copy_board[row][col] == copy_board[row - 2][col + 2] == copy_board[row - 1][col + 1]:
            self.__add_c_move(col - 1)
            return 1
        else:
            return 0

    def __case_8(self, copy_board, row, col):
        ''' the computer analyses the situations where the player has:
                    |0|1|2|3|4|5|6|     |0|1|2|3|4|5|6|     |0|1|2|3|4|5|6|
                    | | | | | | | |     | | | | | | | |     | | | | | | | |
                    |_|_|_|_| | | |     |x|x|x|x| | | |     |x|x|x|x| | | |
                    | |x|x|x|x| | |     | |_|_|_|_| | |     | |x|x|x|x| | |
                    | | |x|x|x|x| |     | | |x|x|x|x| |     | | |_|_|_|_| |
                    | | | |x|x|x|x|     | | | |x|x|x|x|     | | | |x|x|x|x|

            !! and  _        x        x
                     x   or   _   or   x
                      x        x        _
                      (x)       (x)      (x)    is the last move

        and puts its move on "_" if necessary, the coordinates of the computer's last move are updated '''
        if copy_board[row][col] == copy_board[row - 1][col - 1] == copy_board[row - 2][col - 2]:
            if copy_board[row-2][col - 3] != ' ':
                self.__add_c_move(col-3)
                return 1
        elif copy_board[row][col] == copy_board[row - 1][col - 1] == copy_board[row - 3][col - 3]:
            if copy_board[row - 1][col - 2] != ' ':
                self.__add_c_move(col-2)
                return 1
        elif copy_board[row][col] == copy_board[row - 2][col - 2] == copy_board[row - 3][col - 3]:
            self.__add_c_move(col-1)
            return 1
        else:
            return 0

    def __case_9(self, copy_board, row, col):
        ''' the computer analyses the situations where the player has:
                    |0|1|2|3|4|5|6|     |0|1|2|3|4|5|6|     |0|1|2|3|4|5|6|
                    | | | | | | | |     | | | | | | | |     | | | | | | | |
                    | | | | | | | |     | | | | | | | |     | | | | | | | |
                    | | | |_|_|_|_|     | | | |x|x|x|x|     | | | |x|x|x|x|
                    | | |x|x|x|x| |     | | |_|_|_|_| |     | | |x|x|x|x| |
                    | |x|x|x|x| | |     | |x|x|x|x| | |     | |_|_|_|_| | |
                    |x|x|x|x| | | |     |x|x|x|x| | | |     |x|x|x|x| | | |

           !! and       _        x        x
                       x   or  _   or   x
                      x       x        _
                    (x)     (x)      (x)  is the last move

        and puts its move on "_" if necessary, the coordinates of the computer's last move are updated '''
        if copy_board[row][col] == copy_board[row - 1][col + 1] == copy_board[row - 2][col + 2]:
            if copy_board[row-2][col + 3] != ' ':
                self.__add_c_move(col+3)
                return 1
        elif copy_board[row][col] == copy_board[row - 1][col + 1] == copy_board[row - 3][col + 3]:
            if copy_board[row-1][col + 2] != ' ':
                self.__add_c_move(col+2)
                return 1
        elif copy_board[row][col] == copy_board[row - 2][col + 2] == copy_board[row - 3][col + 3]:
            if copy_board[row][col + 1] != ' ':
                self.__add_c_move(col+1)
                return 1
        else:
            return 0


    def add_computer_player_move(self, row_of_palyers_move, column_of_players_move):

        ''' analyses the cases where the human player is about to win and play the move in order to block
         the player's winning move, otherwise if there is nothing to block it makes a random move
         - the coordinates of the computer's last move ar updated
         - the cases in discussion return 1 if the move was blocked and 0 otherwise '''

        copy_board = self.__board_repository.get_board()
        row = row_of_palyers_move
        col = column_of_players_move

        ''' checks on vertical '''
        if self.__first_move_row_comp in [1,2,3]:
            if col != self.__first_move_col_comp:
                if self.__case_1(copy_board, self.__first_move_row_comp, self.__first_move_col_comp) == 1:
                    return

        if row <= 3:
            if self.__case_1(copy_board, row, col) == 1:
                return

        ''' checks on horizontal '''
        for i in range(6):
            for j in range(4):
                if self.__get_row(i, copy_board)[j:j + 4] in [['x', 'x', 'x', ' '], ['o', 'o', 'o', ' ']]:
                    self.__add_c_move(j+3)
                    return
                elif self.__get_row(i, copy_board)[j:j + 4] in [['x', 'x', ' ', 'x'], ['o', 'o', ' ', 'o']]:
                    self.__add_c_move(j+2)
                    return
                elif self.__get_row(i, copy_board)[j:j + 4] in [['x', ' ', 'x', 'x'], ['o', ' ', 'o', 'o']]:
                    self.__add_c_move(j+1)
                    return
                elif self.__get_row(i, copy_board)[j:j + 4] in [[' ', 'x', 'x', 'x'], [' ', 'o', 'o', 'o']]:
                    self.__add_c_move(j)
                    return


        ''' checks on diagonals '''

        if row <= 3 and col in [1, 2, 3, 4]:
            if self.__case_2(copy_board, row, col) == 1:
                return

        if row <= 3 and col in [2, 3, 4, 5]:
            if self.__case_3(copy_board, row, col) == 1:
                return

        if row <= 2 and col in [0, 1, 2, 3]:
            if self.__case_4(copy_board, row, col) == 1:
                return

        if row <= 2 and col in [3, 4, 5, 6]:
            if self.__case_5(copy_board, row, col) == 1:
                return

        if (row >= 2 and row <= 4) and col in [1, 2, 3, 4, 5]:
            if self.__case_6(copy_board, row, col) == 1:
                return

        if (row >= 2 and row <= 4) and col in [1, 2, 3, 4]:
            if self.__case_7(copy_board, row, col) == 1:
                return

        if (row >= 3 and row <= 5) and col in [3, 4, 5, 6]:
            if self.__case_8(copy_board, row, col) == 1:
                return

        if (row >= 3 and row <= 5) and col in [0, 1, 2, 3]:
            if self.__case_9(copy_board, row, col) == 1:
                return

        self.__add_strategy_move(self.__first_move_col_comp, self.__first_move_row_comp, copy_board)
        return

    def __get_all_four_diag_from_a_list(self, list):

        ''' - list = a diagonal with its length bigger than four
            - the function computes each possible consecutive array of four elements an adds it to a list
            - for example from a list [0,1,2,3,4] it will compute [0,1,2,3] and [1,2,3,4]
             - the number of possible arrays of four is len(list) - 3
             - therefore, the final position will always be len(list) - nr_of_lists_that_can_be_formed + 1, where
             len is increased at every list '''

        final_list = []
        nr_of_lists_that_can_be_formed = len(list) - 3
        st = 0
        fin = len(list)
        poz = len(list) - 3
        while nr_of_lists_that_can_be_formed != 0:
            lst = list[st:fin-poz+1]
            fin += 1
            st += 1
            nr_of_lists_that_can_be_formed -= 1
            final_list.append(lst)
        return final_list


    def __get_diagonals(self):

        ''' Function that collects all the diagonals using numpy
            If the diagonals have the required length to win (4) the function adds them to the list of diagonals
            Otherwise, it passes them to a function that extracts all consecutive combinations of four that can be formed '''

        copy_board = self.__board_repository.get_board()
        matrix = numpy.array(copy_board)
        diags = [matrix[::-1,:].diagonal(i) for i in range(-5, 6)]
        diags.extend(matrix.diagonal(i) for i in range(5, -6, -1))
        diag = []
        for n in diags:
            if n.size == 4:
                diag.append(n.tolist())
            elif n.size == 5 or n.size == 6:
                for l in self.__get_all_four_diag_from_a_list(n.tolist()):
                    diag.append(l)
        return diag

    def __get_column(self, index, copy_board):

        ''' function that returns as a list a required column'''

        return [i[index] for i in copy_board]

    def __get_row(self, index, copy_board):

        ''' function that returns as a list a required row'''

        return list(copy_board[index][:])

    def check_win(self):

        ''' function that searches for a winning sequence '''

        copy_board = self.__board_repository.get_board()
        ''' check columns'''

        for i in range(6):
            for j in range(4):
                if self.__get_row(i, copy_board)[j:j+4] in [['x', 'x', 'x', 'x'], ['o', 'o', 'o', 'o']]:
                    return copy_board[i][j]

        ''' Checks rows'''
        for i in range(7):
            for j in range(3):
                if self.__get_column(i, copy_board)[j:j+4] in [['x', 'x', 'x', 'x'], ['o', 'o', 'o', 'o']]:
                    return copy_board[j][i]

        ''' Checks diagonals'''
        for i in self.__get_diagonals():
            for j in range(len(i)):
                if i[j:j + 4] in [['x', 'x', 'x', 'x'], ['o', 'o', 'o', 'o']]:
                    return i[j]
        return None

    def get_the_board(self):
        ''' functions that returns the board '''
        return self.__board_repository.get_board()


