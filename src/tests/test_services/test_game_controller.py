
import unittest

from src.domain.entities import AI
from src.domain.validators import GameControllerDataValidator, MetaException
from src.repository.repo import Squares, Pieces, BaseRepository
from src.services.ai_strategy import AIStrategy
from src.services.game_controller import GameController


class TestGameController(unittest.TestCase):
    def setUp(self):
        self.__pieces = Pieces()
        self.__squares = Squares()
        self.__players = BaseRepository()

        ai_strategy = AIStrategy(self.__pieces, self.__squares)
        self.__players.add(AI(ai_strategy))

        self.__game_controller = GameController(self.__pieces, self.__squares, self.__players,
                                                GameControllerDataValidator)

        self.__game_controller.add_player("steve roger", 1)
        self.__game_controller.add_player("jane doe", 2)

    def test_initialization(self):
        self.assertEqual(self.__game_controller.current_player, "player1")
        self.assertEqual(self.__game_controller.current_player_name, "steve roger")
        piece = self.__game_controller.get_piece_by_id("player1_1")
        self.assertEqual(piece.location, 0)

        self.__game_controller.reset_all()
        self.__game_controller.add_player("player_name", 1)
        self.assertRaises(MetaException, self.__game_controller.add_player, "player_name", 2)

    def test_move(self):
        self.assertEqual(self.__game_controller.current_player, "player1")
        self.__game_controller.roll_dice()
        self.__game_controller.rolled_dice_value = 1
        self.__game_controller.move_piece(1)
        self.assertEqual(self.__game_controller.current_player, "player2")

        new_location = self.__pieces.find_by_id("player1_1").location
        self.assertEqual(new_location, self.__game_controller.rolled_dice_value)

        self.__pieces.find_by_id("player1_1").location = 14
        self.__game_controller.rolled_dice_value = 1

        self.__game_controller.switch_players()
        self.assertEqual(self.__game_controller.current_player, "player1")

        self.__game_controller.move_piece(1)
        new_location = self.__pieces.find_by_id("player1_1").location
        self.assertEqual(new_location, 15)

        self.__game_controller.switch_players()
        self.__pieces.find_by_id("player1_1").location = 6
        self.__pieces.find_by_id("player2_1").location = 7
        self.__game_controller.rolled_dice_value = 1
        self.__game_controller.move_piece(1)
        piece = self.__pieces.find_by_id("player1_2")
        self.assertEqual(piece.location, 0)

    def test_move_exceptions(self):
        self.assertRaises(MetaException, self.__game_controller.move_piece, 1)
        self.__game_controller.roll_dice()
        self.assertRaises(MetaException, self.__game_controller.move_piece, 44)

        self.__pieces.find_by_id("player1_1").location = 2
        self.__pieces.find_by_id("player1_2").location = 4
        self.__game_controller.rolled_dice_value = 2
        self.assertRaises(MetaException, self.__game_controller.move_piece, 1)

        self.__pieces.find_by_id("player1_1").location = 14
        self.__game_controller.rolled_dice_value = 4
        self.assertRaises(MetaException, self.__game_controller.move_piece, 1)

        self.__pieces.find_by_id("player1_1").location = 15
        self.__game_controller.rolled_dice_value = 1
        self.assertRaises(MetaException, self.__game_controller.move_piece, 1)

        self.__pieces.find_by_id("player2_1").location = 8
        self.__pieces.find_by_id("player1_1").location = 7
        self.__game_controller.rolled_dice_value = 1
        self.assertRaises(MetaException, self.__game_controller.move_piece, 1)

    def test_game_control_validator(self):
        self.assertRaises(MetaException, GameControllerDataValidator.validate_number, None)

    def test_win(self):
        self.assertIsNone(self.__game_controller.get_winner_name())
        self.assertFalse(self.__game_controller.win())

        self.__game_controller.player_wins(1)
        self.assertTrue(self.__game_controller.win())
        self.assertEqual(self.__game_controller.winner_name, "steve roger")

    def test_win_player_2(self):
        self.__game_controller.player_wins(2)
        self.assertTrue(self.__game_controller.win())
        self.assertEqual(self.__game_controller.winner_name, "jane doe")

    def test_ai(self):
        self.__game_controller.reset_all()
        self.__game_controller.add_player("john doe", 1)
        self.__game_controller.add_player(None, None, is_human=False)

        self.__game_controller.switch_players()
        self.__game_controller.ai_makes_a_move()

        piece = self.__pieces.find_by_id("player2_1")
        self.assertEqual(piece.location, self.__game_controller.rolled_dice_value)
        piece.location = 0

        self.__game_controller.rolled_dice_value = 0
        self.__game_controller.ai_moves_piece()
        self.assertEqual(piece.location, 0)
