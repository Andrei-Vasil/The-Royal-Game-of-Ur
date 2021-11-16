
import unittest

from src.domain.entities import Player
from src.domain.validators import MetaException
from src.repository.repo import BaseRepository, Pieces, Squares


class TestRepo(unittest.TestCase):
    def test_base_repo(self):
        repo = BaseRepository()
        repo.add(Player(1, "player", "id"))
        repo.replace("id", Player(1, "other_player", "id"))
        self.assertEqual(repo.find_by_id("id").name, "other_player")
        self.assertRaises(MetaException, repo.delete_by_id, "nonexistent id")
        self.assertRaises(MetaException, repo.find_by_id, "nonexistent id")

    def test_pieces(self):
        pieces = Pieces()
        self.assertRaises(MetaException, pieces.initialize_pieces_for_player, 3)

    def test_squares(self):
        squares = Squares()
        self.assertRaises(MetaException, squares.initialize_squares_for_sector, "invalid sector")

