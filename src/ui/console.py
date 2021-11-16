"""
    The console. Want to play the game in the terminal? Weird, but ok, you can do that in here.
"""

from src.domain.validators import MetaException
from src.services.tools import Color


class CommandException(MetaException):
    pass


class Console:
    def __init__(self, board, game_controller):
        self.__board = board
        self.__game_controller = game_controller

        self.__state = "main_menu"

        self.__possible_commands = {"main_menu": {"1": self.__play, "2": self.__switch_ui, "3": self.__quit},
                                    "options": {"1": self.__pvp, "2": self.__pve},
                                    "in_game": {"0": self.__roll_dice, "1": self.__select_piece,
                                                "skip": self.__skip, "quit": self.__quit}
                                    }

        self.__print_menu = {"main_menu": Console.print_main_menu,
                             "options":  Console.print_options_menu,
                             "in_game": self.__get_and_print_in_game_menu
                             }

        self.__in_game_state = ""

        self.__print_in_game_menu = {"new_turn_roll_dice": self.__print_roll_dice_menu,
                                     "dice_rolled_select_piece": self.__print_select_piece_menu
                                     }

        self.__ui = "console"
        self.__skipped = False

    def run(self):
        done = False
        self.__ui = "console"
        while not done:
            if self.__game_controller.win():
                self.__state = "main_menu"
                Console.print_congratulations_message(self.__game_controller.winner_name)
            try:
                command = self.__input_command()
                done = self.__treat_command(command)
            except MetaException as mexc:
                print(Color.RED + str(mexc) + Color.END)

            if self.__ui == "gui":
                break

        return done, self.__ui

    def __input_command(self):
        if self.__skipped:
            return
        self.__print_menu[self.__state]()
        if self.__skipped:
            return

        if self.__game_controller.pve and self.__game_controller.current_player == "player2":
            self.__ai_moves()
            self.__game_controller.switch_players()
            return

        if self.__in_game_state == "dice_rolled_select_piece":
            command = "1"
        else:
            command = input("Please select an option: ")
        return command

    def __treat_command(self, command):
        if self.__skipped:
            self.__skipped = False
            return False
        if self.__game_controller.pve and self.__game_controller.current_player == "player2":
            self.__game_controller.switch_players()
            return False

        if command not in self.__possible_commands[self.__state]:
            raise CommandException("Invalid command given.\n")
        return self.__possible_commands[self.__state][command]()

    def __play(self):
        self.__state = "options"
        return False

    def __roll_dice(self):
        if self.__in_game_state == "dice_rolled_select_piece":
            raise CommandException("You can't select a piece now! You must roll the dice!")

        self.__game_controller.roll_dice()
        self.__in_game_state = "dice_rolled_select_piece"
        return False

    def __skip(self):
        self.__game_controller.switch_players()
        self.__in_game_state = "new_turn_roll_dice"
        self.__skipped = True

        return False

    def __select_piece(self):
        if self.__in_game_state == "new_turn_roll_dice":
            raise CommandException("You need to press 0 in order to roll the dice!")

        piece = input("Type the piece you would like to move " + str(self.__game_controller.rolled_dice_value) +
                      " steps (must be an integer): ")
        if piece == "skip":
            return self.__skip()
        if piece == "quit":
            return self.__quit()
        self.__game_controller.move_piece(piece)
        self.__in_game_state = "new_turn_roll_dice"

        return False

    def __pvp(self):
        self.__game_controller.add_player(input("Please enter first player's name here: "), 1)
        self.__game_controller.add_player(input("Please enter second player's name here: "), 2)
        self.__state = "in_game"
        self.__in_game_state = "new_turn_roll_dice"

    def __pve(self):
        self.__game_controller.add_player(input("Please enter your player name here: "), 1)
        self.__game_controller.add_player(None, None, is_human=False)
        self.__state = "in_game"
        self.__in_game_state = "new_turn_roll_dice"
        return False

    def __ai_moves(self):
        print(Color.BOLD + "\nThe computer is making a move, please wait..." + Color.END)
        self.__game_controller.ai_makes_a_move()

    def __switch_ui(self):
        self.__ui = "gui"
        return False

    def __quit(self):
        return True

    @staticmethod
    def print_main_menu():
        print("Here are your options:\n"
              "1. Play\n"
              "2. Switch UI\n"
              "3. Quit\n"
              )

    @staticmethod
    def print_options_menu():
        print("Please select an option:\n"
              "1. Play against another player (locally)\n"
              "2. Play against the computer\n"
              )

    @staticmethod
    def print_congratulations_message(winner_name):
        print("\n\n" + Color.BOLD + Color.YELLOW + "Congratulations, " + winner_name + ", you have won at the"
              " greatest game there is, The Royal Game of Ur!" + Color.END + "\n\n"
              )

    def __get_and_print_in_game_menu(self):
        self.__print_in_game_menu[self.__in_game_state]()

    def __print_roll_dice_menu(self):
        print("\n\n" + Color.BOLD + "----------------------NEW TURN----------------------" + Color.END)
        print(Color.BOLD + "Remember! You can exit at any time by typing in 'quit'!" + Color.END)
        print(Color.BOLD + "If you can't make any moves, or just don't want to get your pieces exposed, we suggest you"
                           " to skip by typing in 'skip'!" + Color.END)
        print("Here is your freshly minted board:")
        print(self.__board)

        player_color = Color.BLUE
        if self.__game_controller.current_player == "player2":
            player_color = Color.RED
        print("\n" + Color.YELLOW + "It's " + player_color + self.__game_controller.current_player_name + Color.YELLOW +
              "'s turn!" + Color.END)
        print("Press 0 to roll the dice and find out what the universe has prepared for you today!")

    def __print_select_piece_menu(self):
        if 0 <= self.__game_controller.rolled_dice_value <= 1:
            the_way_the_universe_treated_the_player = "The universe was not in your favour today, young traveller..."
        elif 1 < self.__game_controller.rolled_dice_value < 4:
            the_way_the_universe_treated_the_player = "The universe seems impartial for your faith today..."
        elif self.__game_controller.rolled_dice_value == 4:
            the_way_the_universe_treated_the_player = "It seems like the universe cares about you today, take " \
                                                      "advantage of this great opportunity!"
        else:
            raise MetaException("The given dice are not in the valid interval: [0;4]. Your dice were: " +
                                str(self.__game_controller.rolled_dice_value))
        print(the_way_the_universe_treated_the_player + " Your dice value: " +
              str(self.__game_controller.rolled_dice_value))

        if self.__game_controller.rolled_dice_value == 0:
            print(Color.BOLD + "Your rolled dice value was 0. Your turn was automatically skipped. We're very sorry "
                  "for your bad luck :(" + Color.END)
            self.__skip()

    @staticmethod
    def print_goodbye():
        print(Color.BOLD + Color.YELLOW + "\n Hope you enjoyed the greatest game there is, The Royal Game of Ur!!"
              + Color.END)
