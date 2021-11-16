
import unittest

from src.domain.validators import GameControllerDataValidator, MetaException
from src.repository.repo import Pieces, Squares, BaseRepository
from src.services.board import Board
from src.services.game_controller import GameController


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.__pieces = Pieces()
        self.__squares = Squares()
        self.__players = BaseRepository()

        self.__board = Board(self.__pieces)
        self.__game_controller = GameController(self.__pieces, self.__squares, self.__players,
                                                GameControllerDataValidator)

        self.__game_controller.add_player("steve roger", 1)
        self.__game_controller.add_player("jane doe", 2)

        self.__pieces.find_by_id("player1_7").location = 8
        self.__pieces.find_by_id("player1_6").location = 14
        self.__pieces.find_by_id("player1_5").location = 15
        self.__pieces.find_by_id("player1_4").location = 4

        self.__pieces.find_by_id("player2_6").location = 14
        self.__pieces.find_by_id("player2_5").location = 15
        self.__pieces.find_by_id("player2_4").location = 4

    def test_string_format(self):
        board_1 = str(self.__board)

        self.__game_controller.rolled_dice_value = 1
        self.__game_controller.move_piece(1)

        board_2 = str(self.__board)

        self.assertNotEqual(board_1, board_2)

        self.__game_controller.get_piece_by_id("player1_1").location = 0

        board_3 = str(self.__board)

        self.assertEqual(board_1, board_3)

    def test_max_index(self):
        self.assertGreater(self.__board.max_index, 0)

    def test_piece_offsets(self):
        self.assertEqual(self.__board.get_offset_for_piece("player1_7"), (3, 2))
        self.assertEqual(self.__board.get_offset_for_piece("player1_6"), (6, 1))
        self.assertEqual(self.__board.get_offset_for_piece("player1_5"), (12, 1))
        self.assertEqual(self.__board.get_offset_for_piece("player1_4"), (0, 1))
        self.assertEqual(self.__board.get_offset_for_piece("player1_3"), (2, 0))

        self.assertEqual(self.__board.get_offset_for_piece("player2_6"), (6, 3))
        self.assertEqual(self.__board.get_offset_for_piece("player2_5"), (12, 3))
        self.assertEqual(self.__board.get_offset_for_piece("player2_4"), (0, 3))
        self.assertEqual(self.__board.get_offset_for_piece("player2_3"), (2, 4))

        self.assertRaises(MetaException, Board.get_offset, 44, 44, "player1")
