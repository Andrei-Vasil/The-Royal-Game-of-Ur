
from src.domain.validators import MetaException
from src.domain.entities import Piece, Square


class RepoException(MetaException):
    pass


class BaseRepository:
    """
        Stores entities. An entity usually is a player, square or a piece.
    """

    def __init__(self):
        self.__entities = dict()

    def add(self, entity):
        self.__entities[entity.id] = entity

    def replace(self, entity_id, new_entity):
        self.__entities[entity_id] = new_entity

    def delete_by_id(self, entity_id):
        if not self.id_exists(entity_id):
            raise RepoException("No entity found with the given id: " + str(entity_id))
        self.__entities.pop(entity_id)

    def find_by_id(self, entity_id):
        if not self.id_exists(entity_id):
            raise RepoException("No entity found with the given id: " + str(entity_id))
        return self.__entities[entity_id]

    def id_exists(self, entity_id):
        if entity_id in self.__entities:
            return True
        return False

    def get_all(self):
        return self.__entities.values()


class Pieces(BaseRepository):
    """
    This Pieces repository was created specifically to initialize the repo on its creation with the needed pieces for
    each player.
    """
    def __init__(self):
        super().__init__()
        self.initialize_pieces_for_player(1)
        self.initialize_pieces_for_player(2)

    def initialize_pieces_for_player(self, player):
        no_of_pieces = 7
        if not 1 <= player <= 2:
            raise RepoException("Invalid player number given.")
        for i in range(1, no_of_pieces + 1):
            self.add(Piece(i, 0, "player" + str(player)))


class Squares(BaseRepository):
    """
    This Squares repository was created specifically to initialize the repo on its creation with the needed squares for
    each sector.
    """
    def __init__(self):
        super().__init__()
        self.initialize_squares_for_sector("_player1_safezone")
        self.initialize_squares_for_sector("_player2_safezone")
        self.initialize_squares_for_sector("_warzone")

    def initialize_squares_for_sector(self, sector):
        if sector == "_warzone":
            for i in range(5, 13):
                self.add(Square(i, sector))
        elif sector == "_player1_safezone" or sector == "_player2_safezone":
            for i in range(0, 5):
                self.add(Square(i, sector))
            for i in range(13, 16):
                self.add(Square(i, sector))
        else:
            raise RepoException("Invalid sector given.")

    def find_by_location(self, location):
        """
        This is used only to determine whether a square is in a warzone or not (remember, each square is dependant on
        one of the three sectors: _player1_safezone, _player2_safezone or _warzone.
        :param location: integer with the square location
        :return: the required square (if it is in a safezone, it is gonna be in the _player1_safezone)
        """
        for square in self.get_all():
            if square.index == location:
                return square
