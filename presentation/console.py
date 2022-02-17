from errors.exceptions import RepoError, ValidationError
import os
import sys

class UI:

    def __init__(self, Board_Service):
        self.__Board_Service = Board_Service
        self.__commands = {"move": self.__ui_make_a_move,
                           "print_board": self.__ui_print_board,
                         }

        self.__first_random = 0
        self.__won = 0

    def __checks_win(self):
        winner = self.__Board_Service.check_win()
        if winner != None:
            print("Game over!")
            if winner == 'x':
                print("Player has won!")
            elif winner == 'o':
                print("Computer has won!")
            self.__won = 1
            return 1


    def __ui_make_a_move(self, params):
        if len(params) != 2:
            print("invalid number of params!")
            return
        column = int(params[0]) - 1
        piece_type = params[1]
        row = self.__Board_Service.add_player_move(column, piece_type)
        c = self.__checks_win()
        if self.__first_random == 0:
            col_comp, row_comp =self.__Board_Service._add_random()
            self.__Board_Service._keep_positions(col_comp, row_comp)
            self.__first_random += 1
        else:
            self.__Board_Service.add_computer_player_move(row, column)
        board = self.__Board_Service.get_the_board()
        for row in board:
            print('|' + '|'.join(row) + '|')
        if c != 1:
            self.__checks_win()

    def __ui_print_board(self, params):
        if len(params) != 0:
            print("Invalid number of params!")
            return
        board = self.__Board_Service.get_the_board()
        for row in board:
            print('|' + '|'.join(row) + '|')

    def __process_commands(self, cmd):
        # function that processes the command(string) introduced by splitting it into parts
        cmd = cmd.strip()
        parts = cmd.split()
        cmd_name = parts[0]
        params = parts[1:]
        return cmd_name, params

    def run(self):
        while True:
            cmd = input(">>>")
            cmd = cmd.strip()
            if cmd == "":
                continue
            cmd_name, params = self.__process_commands(cmd)
            if cmd_name == "exit":
                print("Done")
                return
            elif cmd_name in self.__commands:
                try:
                    self.__commands[cmd_name](params)
                except ValueError as ve:
                    print("invalid numerical input")
                except RepoError as re:
                    print(str(re))
                except ValidationError as ve:
                    print("Validation error:" + str(ve))
                if self.__won == 1:
                    restart = input("\nDo you want to restart the game? [yes/no] ")
                    if restart == "yes":
                        os.system('python "C:/Users/Stefania/PycharmProjects/pythonProject_assignment11/main.py"')
                    else:
                        return
            else:
                print("invalid command")
