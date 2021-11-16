"""
    The manager of the game. It does everything!
"""

import traceback

from src.domain.entities import AI
from src.domain.validators import MetaException, GameControllerDataValidator
from src.repository.repo import Pieces, Squares, BaseRepository
from src.services.ai_strategy import AIStrategy
from src.services.board import Board
from src.services.game_controller import GameController
from src.services.tools import Color
from src.ui.console import Console
from src.ui.gui import GUI


class Manager:
    """
        The manager of the game. It does everything!
        Important services:
            __game_controller, __board
        Important ui:
            __gui, __console
    """
    def __init__(self):
        # repos:
        self.__pieces = Pieces()
        self.__squares = Squares()
        self.__players = BaseRepository()

        # services:
        self.__board = Board(self.__pieces)
        self.__game_controller = GameController(self.__pieces, self.__squares, self.__players,
                                                GameControllerDataValidator)
        ai_strategy = AIStrategy(self.__pieces, self.__squares)

        # ui:
        self.__console = Console(self.__board, self.__game_controller)
        self.__gui = GUI(self.__board, self.__game_controller)

        # add AI to players:
        self.__players.add(AI(ai_strategy))

    def run(self) -> None:
        """
            Call this when you want to play the game!
        """
        done = False
        ui = "gui"
        while not done:
            if ui == "console":
                done, ui = self.__console.run()
            elif ui == "gui":
                done, ui = self.__gui.run()
            else:
                raise MetaException("Error: Invalid UI given.")
        Console.print_goodbye()


if __name__ == "__main__":
    try:
        manager = Manager()
        manager.run()
    except MetaException as ex:
        traceback.print_exc()
        print(Color.RED + str(ex) + Color.END)
