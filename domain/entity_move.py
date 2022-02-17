class Move:
    def __init__(self,column, piece_type):
        self.__column = column
        self.__piece_type = piece_type

    def get_column(self):
        return self.__column

    def get_piece_type(self):
        return self.__piece_type

    def set_piece_type(self, value):
        self.__piece_type = value
