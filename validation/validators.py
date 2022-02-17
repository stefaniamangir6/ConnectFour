from errors.exceptions import ValidationError

class Move_Validator:

    def __init__(self):
        pass

    def validate(self, move):
        errors = ""
        if move.get_column() < 0 or move.get_column() > 6:
            errors += "invalid column!\n"
        if move.get_piece_type() != "x" or move.get_piece_type() == "":
            errors += "invalid name!\n"
        if len(errors) > 0:
            raise ValidationError(errors)
