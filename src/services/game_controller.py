
import time
from src.domain.entities import Player
from src.domain.validators import MetaException
from src.services.tools import RandomGenerator


class DuplicationException(MetaException):
    pass


class GameController:
    """
        Game Controller. Takes care that nobody is cheating at The Royal Game of Ur!
    """
    def __init__(self, pieces, squares, players, game_controller_validator):
        """
        :param pieces: pieces repository
        :param squares: squares repository
        :param players: players repository
        :param game_controller_validator: game validator class
        """
        self.__pieces = pieces
        self.__squares = squares
        self.__players = players

        self.__game_controller_validator = game_controller_validator

        self.__current_player_name = ""
        self.__current_player = "player1"

        self.__winner_name = None
        self.pve = False

        self.rolled_dice_value = 0

    @property
    def current_player(self) -> str:
        return self.__current_player

    @current_player.setter
    def current_player(self, next_player) -> None:
        self.__current_player = next_player
        player_number_str = next_player[-1]
        self.__current_player_name = self.get_name_for_player(player_number_str)

    @property
    def current_player_name(self) -> str:
        return self.__current_player_name

    @property
    def winner_name(self) -> str:
        return self.__winner_name

    def get_piece_by_id(self, piece_id):
        return self.__pieces.find_by_id(piece_id)

    def add_player(self, player_name, player_number, is_human=True) -> None:
        """
        Adds a player to the game. If the player is not human, it sets the pve True.
        :param player_name: any name you want!
        :param player_number: 1 or 2
        :param is_human: True or False
        """
        if not is_human:
            self.pve = True
            self.__players.find_by_id("computer").number = 2
            return
        if player_number == 1:
            self.__current_player_name = player_name
        id_ = RandomGenerator.generate_string()
        stepped_over = False
        while self.__players.id_exists(id_) or stepped_over is False:
            id_ = RandomGenerator.generate_string()
            stepped_over = True
        for player in self.__players.get_all():
            if player.name == player_name:
                self.reset_all()
                raise DuplicationException("The 2 players can't have the same name!")
        self.__players.add(Player(player_number, player_name, id_))

    def roll_dice(self) -> None:
        """
        Rolls the dice. Fixes rolled_dice_value, randomly, to a value between 0 and no_of_dice.
        no_of_dice is usually 4, but it can be set by the developer to whatever he/she might wish.
        """
        self.rolled_dice_value = 0
        no_of_dice = 4
        for i in range(no_of_dice):
            generated_side = RandomGenerator.generate_number(1, 4)
            if generated_side == 2 or generated_side == 4:
                self.rolled_dice_value += 1

    def move_piece(self, piece_number) -> None:
        """
        Move a piece, any piece! The piece's location gets updated += rolled_dice_value
        :param piece_number: piece's index the player desires to move.
        """
        self.__game_controller_validator.validate_number(piece_number)

        piece_number = int(piece_number)
        self.__game_controller_validator.check_if_piece_can_be_moved(piece_number, self.__pieces, self.current_player,
                                                                     self.rolled_dice_value
                                                                     )
        piece = self.__pieces.find_by_id(self.current_player + "_" + str(piece_number))
        new_location = piece.location + self.rolled_dice_value

        if new_location == 15:  # the piece reached the end
            piece.location = new_location
            self.switch_players()
            return

        for existing_piece in self.__pieces.get_all():
            if existing_piece.location == new_location and self.__squares.find_by_location(new_location).is_warzone:
                self.__pieces.find_by_id(existing_piece.id).location = 0
        piece.location = new_location

        if 4 < new_location < 13:
            sector = "_warzone"
        else:
            sector = "_" + self.current_player + "_safezone"
        current_square = self.__squares.find_by_id(str(new_location) + sector)
        if not current_square.is_double_throw:
            self.switch_players()

    def win(self) -> bool:
        """
        Did somebody win yet?
        :return: True or False
        """
        self.__winner_name = self.get_winner_name()
        if self.__winner_name is None:
            return False
        return True

    def get_winner_name(self):
        """
        Hurray! Somebody won! What is his/her name?
        :return: winner's name; if there isn't any winner, it returns None
        """
        if self.get_winner() is None:
            return None

        winner_number = int(self.get_winner()[-1])
        for player in self.__players.get_all():
            if player.number == winner_number:
                player.increment_wins()
                self.reset_all()
                return player.name

    def get_winner(self):
        """
        This method actually goes through the repo and sees if anybody has all their pieces on the end squares.
        :return: "player1"/"player2". In case nobody won yet, it returns None.
        """
        no_of_pieces = len(self.__pieces.get_all())/2
        end_pieces = {"player1": 0, "player2": 0}
        for piece in self.__pieces.get_all():
            if piece.state == "finish":
                end_pieces[piece.id.split("_")[0]] += 1
        if end_pieces["player1"] == no_of_pieces:
            return "player1"
        elif end_pieces["player2"] == no_of_pieces:
            return "player2"
        return None

    def get_name_for_player(self, player_number) -> str:
        """
        :param player_number: 1 or 2
        :return: whatever the names for "player1"/"player2" are.
        """
        self.__game_controller_validator.validate_number(player_number)
        player_number = int(player_number)
        for player in self.__players.get_all():
            if player.number == player_number:
                return player.name

    def reset_all(self) -> None:
        """
        Reset everything!
        By default, pve is False. AI player is out of the game (computer.number = 0).
        All players that are not AI get deleted. This, of course, can be changed in case one might wish to implement
        a leaderboard system.
        All pieces get back to spawn.
        """
        self.pve = False
        if self.__players.id_exists("computer"):
            self.__players.find_by_id("computer").number = 0
        for piece in self.__pieces.get_all():
            piece.location = 0
        player_ids_to_remove = []
        for player in self.__players.get_all():
            if player.id != "computer":
                player_ids_to_remove.append(player.id)
        for player_id in player_ids_to_remove:
            self.__players.delete_by_id(player_id)

    def switch_players(self) -> None:
        """
        Come on, it's my turn!
        Players switch turns so everybody gets a chance at The Royal Game of Ur!
        """
        new_player = "player1"
        if self.current_player == "player1":
            new_player = "player2"
        self.current_player = new_player

    def ai_makes_a_move(self) -> None:
        """
        The AI make a move.
        He rolls his own dice, and moves his own pieces.
        """
        no_of_seconds_to_sleep = 1
        time.sleep(no_of_seconds_to_sleep)

        self.roll_dice()
        self.ai_moves_piece()

    def ai_moves_piece(self) -> None:
        """
        So the AI decided to move a piece.
        If he can't move any, he will skip.
        If he can in fact move, his piece will get relocated to its location + rolled_dice_value
        """
        ai = self.__players.find_by_id("computer")
        if not ai.can_make_move(self.rolled_dice_value):
            self.switch_players()
            return
        self.move_piece(ai.get_piece_number_to_move(self.rolled_dice_value))

    def player_wins(self, player_number: int) -> None:
        """
        This is a cheat method. We don't like cheaters, but this helps us out on tests. If you want any player to win,
        just call this method and all his/her pieces teleport to the end squares!
        :param player_number: 1 or 2
        """
        player = "player" + str(player_number)
        index = 1
        piece_id = player + "_" + str(index)
        while self.__pieces.id_exists(piece_id):
            self.__pieces.find_by_id(piece_id).location = 15
            index += 1
            piece_id = player + "_" + str(index)
