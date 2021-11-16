

class MetaException(Exception):
    pass


class EntityException(MetaException):
    pass


class GameControllerException(MetaException):
    pass


class GameControllerDataValidator:
    @staticmethod
    def check_if_piece_can_be_moved(piece_number, pieces, current_player, rolled_dice_value) -> None:
        """
        If the player decided to move a piece that can't be moved, an exception will be raised!
        :param piece_number: the piece number you want to check if it can be moved
        :param pieces: all the pieces in the game (repository which is also in game controller)
        :param current_player: who is the current player? "player1"/"player2"
        :param rolled_dice_value: the dice value that the player has to work with (i.e. how many steps will the piece
        move)
        """
        piece_id = current_player + "_" + str(piece_number)
        if not pieces.id_exists(piece_id):
            raise GameControllerException("There is no piece with the given index number!")

        piece = pieces.find_by_id(piece_id)
        if piece.state == "finish":
            raise GameControllerException("You can't move pieces that are out of the game!")

        new_location = piece.location + rolled_dice_value
        if new_location > 15:
            raise GameControllerException("The rolled value is too high for you to move this piece!")
        for existing_piece in pieces.get_all():
            if new_location == existing_piece.location == 8 and not existing_piece.owner == current_player:
                raise GameControllerException("You can't take over the pieces of another player while they are on "
                                              "the safe spot!")
            if existing_piece.location == new_location and new_location != 15 and existing_piece.owner == \
                    current_player:
                raise GameControllerException("You can't have more than one piece on a square at a time!")

    @staticmethod
    def validate_number(piece_number) -> None:
        """
        If the player gave a number that is not really an integer, an exception will be raised!
        :param piece_number: the piece number you want to validate
        """
        try:
            int(piece_number)
        except Exception:
            raise GameControllerException("PieceRect number must be an integer! " + str(type(piece_number)) +
                                          " instead given.")
