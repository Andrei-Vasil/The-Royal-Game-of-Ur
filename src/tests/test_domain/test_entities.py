
import unittest

from src.domain.entities import Player, Square
from src.domain.validators import MetaException


class TestEntities(unittest.TestCase):
    def test_player(self):
        player = Player(1, "john", "id")
        self.assertEqual(player.wins, 0)
        self.assertRaises(MetaException, Player, 1, "", "id")
        self.assertRaises(MetaException, Player, 1, "#%&#", "id")

    def test_piece(self):
        piece = Square(0, "_player1_safezone")
        self.assertTrue(piece.is_start)
