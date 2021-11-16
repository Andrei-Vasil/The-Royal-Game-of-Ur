
from src.domain.validators import MetaException


class AIException(MetaException):
    pass


class AIStrategy:
    """
        The AI Strategy. Gives a brain to the computer player.
    """
    def __init__(self, pieces, squares):
        """
        :param pieces: requires the pieces repository that is also assigned to game_controller
        :param squares: requires the squares repository that is also assigned to game_controller
        """
        self.__pieces = pieces
        self.__squares = squares
        self.__max_index = self.__determine_max_index()

    def __determine_max_index(self) -> int:
        """
        :return: the maximum index any piece has (most usually 7, in the case of the classic game)
        """
        max_index = 0
        for piece in self.__pieces.get_all():
            max_index = max(max_index, piece.index)
        return max_index

    def get_best_piece_number_to_move(self, rolled_dice_value) -> str:
        """
        :param rolled_dice_value: the dice value that the ai has to work with (i.e. how many steps will the piece move)
        :return: this returns the best piece the ai player can move, as a number (string format)
        """
        piece_ids = ["player2_" + str(index + 1) for index in range(self.__max_index)]
        max_id = None
        max_score = 0
        for piece_id in piece_ids:
            piece_score = self.__get_points_for(piece_id, rolled_dice_value)
            if piece_score > max_score:
                max_score = piece_score
                max_id = piece_id
        if max_id is None:
            raise AIException("Something went terribly wrong. AI found no piece to move!")
        piece_number = max_id.split("_")[1]
        return piece_number

    def __get_points_for(self, piece_id, rolled_dice_value) -> int:
        """
        :param piece_id: the piece id ("player" + player_number + "_" + piece_index)
        :param rolled_dice_value: the dice value that the ai has to work with (i.e. how many steps will the piece move)
        :return: returns a value which assigned to each piece, according to the minimax algorithm. It ranges between
        -1 (can't move) to 100 (I can move and if I do so I am one step closer to a win)
        """
        piece = self.__pieces.find_by_id(piece_id)
        if not self.__can_move(piece, rolled_dice_value):
            return -1
        if self.__can_finish(piece, rolled_dice_value):
            return 100
        if self.__can_get_to_safe_spot(piece, rolled_dice_value):
            return 50
        if self.__can_attack_enemy(piece, rolled_dice_value):
            return 40
        if self.__can_get_to_double_throw(piece, rolled_dice_value):
            return 30
        if self.__can_get_to_safety(piece, rolled_dice_value):
            return 20
        if self.__can_move(piece, rolled_dice_value):
            return 10

    def __can_finish(self, piece, rolled_dice_value) -> bool:
        """
        :param piece: a piece object (the piece you want to test)
        :param rolled_dice_value: the dice value that the ai has to work with (i.e. how many steps will the piece move)
        :return: whether or not the piece can finish the game with the assigned rolled dice value
        """
        future_square = self.__get_square(piece.location + rolled_dice_value, "player2")
        return future_square.is_end

    def __can_get_to_safe_spot(self, piece, rolled_dice_value) -> bool:
        """
        The safe spot is the 4th square on the middle row (a.k.a. warzone)
        :param piece: a piece object (the piece you want to test)
        :param rolled_dice_value: the dice value that the ai has to work with (i.e. how many steps will the piece move)
        :return: whether or not the piece can get to the safe spot with the assigned rolled dice value
        """
        future_square = self.__get_square(piece.location + rolled_dice_value, "player2")
        conditions = [future_square.is_safe_spot, not self.__there_are_other_team_pieces(piece, rolled_dice_value),
                      not self.__there_are_same_team_pieces(piece, rolled_dice_value)
                      ]
        result = True
        for condition in conditions:
            result = result and condition
        return result

    def __can_attack_enemy(self, piece, rolled_dice_value) -> bool:
        """
        When you attack an enemy piece, that piece gets back to spawn.
        :param piece: a piece object (the piece you want to test)
        :param rolled_dice_value: the dice value that the ai has to work with (i.e. how many steps will the piece move)
        :return: whether or not the piece can attack an enemy piece with the assigned rolled dice value
        """
        future_square = self.__get_square(piece.location + rolled_dice_value, "player2")
        conditions = [future_square.is_warzone, not future_square.is_safe_spot,
                      self.__there_are_other_team_pieces(piece, rolled_dice_value),
                      not self.__there_are_same_team_pieces(piece, rolled_dice_value)
                      ]
        result = True
        for condition in conditions:
            result = result and condition
        return result

    def __can_get_to_double_throw(self, piece, rolled_dice_value) -> bool:
        """
        "The double throw" is a spot on the board where, if the player lands on it, he/she is allowed to throw one more
        time
        :param piece: a piece object (the piece you want to test)
        :param rolled_dice_value: the dice value that the ai has to work with (i.e. how many steps will the piece move)
        :return: whether or not the piece can get to double throw with the assigned rolled dice value
        """
        future_square = self.__get_square(piece.location + rolled_dice_value, "player2")
        conditions = [future_square.is_double_throw, not self.__there_are_same_team_pieces(piece, rolled_dice_value)]
        result = True
        for condition in conditions:
            result = result and condition
        return result

    def __can_get_to_safety(self, piece, rolled_dice_value) -> bool:
        """
        Safety are the first 4 squares and the last 2 squares; a.k.a. the squares out of the warzone (in the safezone)
        :param piece: a piece object (the piece you want to test)
        :param rolled_dice_value: the dice value that the ai has to work with (i.e. how many steps will the piece move)
        :return: whether or not the piece can get to safety with the assigned rolled dice value
        """
        future_square = self.__get_square(piece.location + rolled_dice_value, "player2")
        conditions = [not future_square.is_warzone,
                      not self.__there_are_same_team_pieces(piece, rolled_dice_value)
                      ]
        result = True
        for condition in conditions:
            result = result and condition
        return result

    def __can_move(self, piece, rolled_dice_value) -> bool:
        """
        :param piece: a piece object (the piece you want to test)
        :param rolled_dice_value: the dice value that the ai has to work with (i.e. how many steps will the piece move)
        :return: whether or not the piece can move; anywhere
        """
        return self.__piece_can_make_move(piece, rolled_dice_value)

    def __get_square(self, location, player):
        """
        :param location: a number (integer/string) between 0 and 15
        :param player: which sector would you like? remember, square id is also dependant on the player!
        square 2 for player1 is not the same as square 2 for player2!
        :return: a square object
        """
        sector = "_warzone"
        if not 5 <= location <= 12:
            sector = "_" + player + "_safezone"
        square_id = str(location) + sector
        return self.__squares.find_by_id(square_id)

    def __there_are_same_team_pieces(self, piece, rolled_dice_value) -> bool:
        """
        :param piece: a piece object (the piece you want to move)
        :param rolled_dice_value: the dice value that the ai has to work with (i.e. how many steps will the piece move)
        :return: whether there are any same team pieces on piece.location + rolled_dice_value square or not
        """
        there_are_same_team_pieces = False
        for other_piece in self.__pieces.get_all():
            if other_piece.owner == piece.owner and other_piece.location == piece.location + rolled_dice_value:
                there_are_same_team_pieces = True
        return there_are_same_team_pieces

    def __there_are_other_team_pieces(self, piece, rolled_dice_value) -> bool:
        """
        :param piece: a piece object (the piece you want to move)
        :param rolled_dice_value: the dice value that the ai has to work with (i.e. how many steps will the piece move)
        :return: whether there are any other team pieces on piece.location + rolled_dice_value square or not
        """
        other_team_owner = "player1"
        """
        # in case you want ai vs ai:
        if piece.owner == "player1":
            other_team_owner = "player2"
        """

        there_are_other_team_pieces = False
        for other_piece in self.__pieces.get_all():
            if other_piece.owner == other_team_owner and other_piece.location == piece.location + rolled_dice_value:
                there_are_other_team_pieces = True
        return there_are_other_team_pieces

    def can_make_move(self, rolled_dice_value) -> bool:
        """
        :param rolled_dice_value: the dice value that the ai has to work with (i.e. how many steps will the piece move)
        :return: can the ai make a move at all?
        """
        if rolled_dice_value == 0:
            return False
        can_make_move = False
        for piece in self.__pieces.get_all():
            if piece.owner == "player2":
                can_make_move = can_make_move or self.__piece_can_make_move(piece, rolled_dice_value)
        return can_make_move

    def __piece_can_make_move(self, piece, rolled_dice_value) -> bool:
        """
        :param piece: a piece object (the piece you want to see if it can make a move)
        :param rolled_dice_value: the dice value that the ai has to work with (i.e. how many steps will the piece move)
        :return: can the ai move this piece? anywhere is good, really
        """
        if piece.location + rolled_dice_value == 15:
            return True
        if piece.location + rolled_dice_value > 15:
            return False
        if self.__there_are_same_team_pieces(piece, rolled_dice_value):
            return False
        future_square = self.__get_square(piece.location + rolled_dice_value, "player2")
        if self.__there_are_other_team_pieces(piece, rolled_dice_value) and future_square.is_safe_spot:
            return False
        return True
