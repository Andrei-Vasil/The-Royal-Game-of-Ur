
from src.domain.validators import EntityException


class BaseEntity:
    def __init__(self, id_: any):
        self.__id = id_

    @property
    def id(self):
        return self.__id


class Player(BaseEntity):
    """
        A player. Has a name, a number (1 or 2 when in match, 0 when not in a match) and an id!
    """
    def __init__(self, number: int, name: str, id_: str):
        """
        :param id_: str = any
        :param number: int = "1"|"2"
        :param name: str = any
        """
        super().__init__(id_)

        if not name.strip():
            raise EntityException("Player name can't be empty!")
        banned_chars = "#$%^&*()+=\\|;:\"?><.,/!@~`"
        for banned_char in banned_chars:
            if banned_char in name:
                raise EntityException("Banned char added to player's name!")
        self.number = number
        self.name = name
        self.__wins = 0

    @property
    def wins(self) -> int:
        """
        This method has no use yet, but if the developer chooses to implement a leaderboard system, this could be useful
        later on.
        :return: how many wins does this player has?
        """
        return self.__wins

    def increment_wins(self) -> None:
        """
        After the player wins a match, you might want to increment his wins to += 1 !
        """
        self.__wins += 1


class AI(Player):
    """
        The AI player. If you want to play against the computer, choose this entity to make the moves!
    """
    def __init__(self, strategy):
        super().__init__(0, "computer", "computer")
        self.__strategy = strategy

    def get_piece_number_to_move(self, rolled_dice_value) -> str:
        """
        If the AI can make a move, he should select the best one he can move with the dice value he got.
        :param rolled_dice_value: the dice value that the ai has to work with (i.e. how many steps will the piece move)
        :return: the number of the piece the ai selected to move. Remember, it returns it as a string!
        """
        return self.__strategy.get_best_piece_number_to_move(rolled_dice_value)

    def can_make_move(self, rolled_dice_value) -> bool:
        """
        Can the AI make a move? If he is stuck, he might want to skip his turn!
        :param rolled_dice_value: the dice value that the ai has to work with (i.e. how many steps will the piece move)
        :return: whether or not the AI can make a move
        """
        return self.__strategy.can_make_move(rolled_dice_value)


class Square(BaseEntity):
    def __init__(self, index: int, sector: str):
        """
        :param index: int = 0 -> 14
        :param sector: str = "_warzone"/"_player1_safezone"/"_player2_safezone"

        Object properties:
        -id: str = str(index) + sector
        -index: int = index
        -is_start: bool
        -is_safe_spot: bool
        -is_end: bool
        -is_warzone: bool
        -is_double_throw: bool
        """
        super().__init__(str(index) + sector)
        self.__index = index
        self.__sector = sector
        self.__decide_if_special_spot()

    def __decide_if_special_spot(self) -> None:
        """
        Special spots are:
        start -> index 0
        end -> index 15
        safe spot -> index 8
        warzone -> index 5->12
        double throw -> index 4, 8, 14
        """
        self.__is_start = self.__is_end = self.__is_safe_spot = self.__is_warzone = self.__is_double_throw = False
        if 4 < self.__index < 13:
            self.__is_warzone = True
        if self.__index == 0:
            self.__is_start = True
        if self.__index == 15:
            self.__is_end = True
        if self.__index == 8:
            self.__is_safe_spot = True
        if self.__index == 4 or self.__index == 8 or self.__index == 14:
            self.__is_double_throw = True

    @property
    def index(self):
        return self.__index

    @property
    def is_start(self):
        return self.__is_start

    @property
    def is_warzone(self):
        return self.__is_warzone

    @property
    def is_safe_spot(self):
        return self.__is_safe_spot

    @property
    def is_double_throw(self):
        return self.__is_double_throw

    @property
    def is_end(self):
        return self.__is_end


class Piece(BaseEntity):
    def __init__(self, id_: int, location: int, owner: str):
        """
        :param id_: int = 1 -> 7
        :param location: int = 0 -> 15
        :param owner: str = "player1/player2"
        -id becomes: [player]_[id_]
        -state: str = "spawn"/"in_game"/"finish"
        -index: int = id_
        """
        super().__init__(owner + "_" + str(id_))
        self.__location = location
        self.__owner = owner.lower()
        self.__index = id_
        self.__update_state()

    def __update_state(self) -> None:
        """
        When the location changes, you might also want to change piece's state, it can change a lot during the game!
        """
        if self.__location == 0:
            self.__state = "spawn"
        elif self.__location == 15:
            self.__state = "finish"
        else:
            self.__state = "in_game"

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, location):
        self.__location = location
        self.__update_state()

    @property
    def index(self):
        return self.__index

    @property
    def owner(self):
        return self.__owner

    @property
    def state(self):
        return self.__state
