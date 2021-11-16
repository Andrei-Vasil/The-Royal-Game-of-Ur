
import unittest

from src.domain.validators import MetaException
from src.repository.repo import Pieces, Squares
from src.services.ai_strategy import AIStrategy


class TestAIStrategy(unittest.TestCase):
    def setUp(self):
        self.__pieces = Pieces()
        self.__squares = Squares()

        self.__ai_strategy = AIStrategy(self.__pieces, self.__squares)

    def test_finish(self):
        self.__pieces.find_by_id("player2_1").location = 14
        piece_number = self.__ai_strategy.get_best_piece_number_to_move(1)
        self.assertEqual(piece_number, "1")

    def test_safe_spot(self):
        self.__pieces.find_by_id("player2_1").location = 7
        piece_number = self.__ai_strategy.get_best_piece_number_to_move(1)
        self.assertEqual(piece_number, "1")

    def test_enemy_attack(self):
        self.__pieces.find_by_id("player2_1").location = 6
        self.__pieces.find_by_id("player1_1").location = 7
        piece_number = self.__ai_strategy.get_best_piece_number_to_move(1)
        self.assertEqual(piece_number, "1")

    def test_double_throw(self):
        self.__pieces.find_by_id("player2_1").location = 3
        piece_number = self.__ai_strategy.get_best_piece_number_to_move(1)
        self.assertEqual(piece_number, "1")

    def test_safety(self):
        self.__pieces.find_by_id("player2_1").location = 12
        piece_number = self.__ai_strategy.get_best_piece_number_to_move(1)
        self.assertEqual(piece_number, "1")
        self.__pieces.find_by_id("player2_1").location = 0
        piece_number = self.__ai_strategy.get_best_piece_number_to_move(1)
        self.assertEqual(piece_number, "1")

    def test_10_pointers(self):
        index = 2
        piece_id = "player2_" + str(index)
        while self.__pieces.id_exists(piece_id):
            self.__pieces.find_by_id(piece_id).location = 15
            index += 1
            piece_id = "player2_" + str(index)
        self.__pieces.find_by_id("player2_1").location = 4
        piece_number = self.__ai_strategy.get_best_piece_number_to_move(1)
        self.assertEqual(piece_number, "1")

    def test_no_moves_left(self):
        index = 1
        piece_id = "player2_" + str(index)
        while self.__pieces.id_exists(piece_id):
            self.__pieces.find_by_id(piece_id).location = 15
            index += 1
            piece_id = "player2_" + str(index)
        self.assertRaises(MetaException, self.__ai_strategy.get_best_piece_number_to_move, 1)

    def test_best_move_cant_happen(self):
        self.__pieces.find_by_id("player2_1").location = 4
        self.__pieces.find_by_id("player1_1").location = 8
        self.__pieces.find_by_id("player2_2").location = 3
        self.__pieces.find_by_id("player2_3").location = 7
        self.assertEqual(self.__ai_strategy.get_best_piece_number_to_move(1), '4')
