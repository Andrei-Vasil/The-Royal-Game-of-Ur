
import pygame

from src.domain.validators import MetaException
from src.ui.clickables import Button, PieceRect, MovePieceRect
from src.ui.input_box import InputBox
from src.ui.window import WindowSize
from src.ui.colors import RGB


class Menu:
    def __init__(self, master, fonts, rel_folder_path):
        self._master = master
        self._fonts = fonts
        self._rel_folder_path = rel_folder_path


class MainMenu(Menu):
    def __init__(self, master, fonts, rel_folder_path):
        super().__init__(master, fonts, rel_folder_path)
        self.play_button = Button(RGB.BEIGE, WindowSize.WIDTH / 2, 120, 140, 50, text="Play!", border_width=2)
        self.switch_ui_button = Button(RGB.BEIGE, WindowSize.WIDTH / 2, 220, 140, 50, text="Switch UI", border_width=2)
        self.quit_button = Button(RGB.BEIGE, WindowSize.WIDTH / 2, 320, 140, 50, text="Quit", border_width=2)

    def draw_title(self):
        title_background_surface = pygame.image.load(self._rel_folder_path + "title-paper.png")
        title_background_surface = pygame.transform.scale(title_background_surface, (440, 90))
        title_background_rect = title_background_surface.get_rect(center=(WindowSize.WIDTH / 2, 55))
        self._master.blit(title_background_surface, title_background_rect)

        title_surface = self._fonts.BIG_TEXT.render("The Royal Game of Ur", True, RGB.BLACK)
        title_rect = title_surface.get_rect(center=(WindowSize.WIDTH / 2, 55))
        self._master.blit(title_surface, title_rect)

    def draw_buttons(self):
        self.play_button.draw(self._master, self._fonts)
        self.switch_ui_button.draw(self._master, self._fonts)
        self.quit_button.draw(self._master, self._fonts)


class OptionsMenu(Menu):
    def __init__(self, master, fonts, rel_folder_path):
        super().__init__(master, fonts, rel_folder_path)
        self.pvp_button = Button(RGB.BEIGE, WindowSize.WIDTH / 2, 120, 300, 50, text="Play against another player",
                                 border_width=2)
        self.pve_button = Button(RGB.BEIGE, WindowSize.WIDTH / 2, 220, 300, 50, text="Play against the computer",
                                 border_width=2)

    def draw_title(self):
        title_background_surface = pygame.image.load(self._rel_folder_path + "title-paper.png")
        title_background_surface = pygame.transform.scale(title_background_surface, (440, 90))
        title_background_rect = title_background_surface.get_rect(center=(WindowSize.WIDTH / 2, 55))
        self._master.blit(title_background_surface, title_background_rect)

        title_surface = self._fonts.BIG_TEXT.render("Pick an opponent: ", True, RGB.BLACK)
        title_rect = title_surface.get_rect(center=(WindowSize.WIDTH / 2, 55))
        self._master.blit(title_surface, title_rect)

    def draw_buttons(self):
        self.pvp_button.draw(self._master, self._fonts)
        self.pve_button.draw(self._master, self._fonts)


class PVPMenu(Menu):
    def __init__(self, master, fonts, rel_folder_path):
        super().__init__(master, fonts, rel_folder_path)
        self.first_player_name = InputBox(WindowSize.WIDTH / 2 + 125, 50, 150, 26)
        self.second_player_name = InputBox(WindowSize.WIDTH / 2 + 125, 150, 150, 26)
        self.pvp_button = Button(RGB.BEIGE, WindowSize.WIDTH / 2, 225, 120, 50, text="Play!", border_width=2)

    def draw_text(self):
        title_background_surface = pygame.image.load(self._rel_folder_path + "title-paper.png")
        title_background_surface = pygame.transform.scale(title_background_surface, (440, 90))
        title_background_rect = title_background_surface.get_rect(
            center=(WindowSize.WIDTH / 2 - 200, 50)
        )
        self._master.blit(title_background_surface, title_background_rect)

        title_background_surface = pygame.image.load(self._rel_folder_path + "title-paper.png")
        title_background_surface = pygame.transform.scale(title_background_surface, (440, 90))
        title_background_rect = title_background_surface.get_rect(
            center=(WindowSize.WIDTH / 2 - 200, 150)
        )
        self._master.blit(title_background_surface, title_background_rect)

        first_player_surface = self._fonts.BIG_TEXT.render("First player's name: ", True, RGB.BLACK)
        first_player_rect = first_player_surface.get_rect(
            center=(WindowSize.WIDTH / 2 - 200, 50)
        )
        self._master.blit(first_player_surface, first_player_rect)

        second_player_surface = self._fonts.BIG_TEXT.render("Second player's name: ", True, RGB.BLACK)
        second_player_rect = second_player_surface.get_rect(
            center=(WindowSize.WIDTH / 2 - 200, 150)
        )
        self._master.blit(second_player_surface, second_player_rect)

    def draw_input_boxes(self):
        self.first_player_name.draw(self._master, self._fonts)
        self.second_player_name.draw(self._master, self._fonts)

    def draw_buttons(self):
        self.pvp_button.draw(self._master, self._fonts)

    def display_error(self, error_msg):
        title_background_surface = pygame.image.load(self._rel_folder_path + "title-paper.png")
        title_background_surface = pygame.transform.scale(title_background_surface, (700, 90))
        title_background_rect = title_background_surface.get_rect(center=(WindowSize.WIDTH / 2, WindowSize.HEIGHT - 65))
        self._master.blit(title_background_surface, title_background_rect)

        title_surface = self._fonts.BIG_TEXT.render(error_msg, True, RGB.RED)
        title_rect = title_surface.get_rect(center=(WindowSize.WIDTH / 2, WindowSize.HEIGHT - 65))
        self._master.blit(title_surface, title_rect)


class PVEMenu(Menu):
    def __init__(self, master, fonts, rel_folder_path):
        super().__init__(master, fonts, rel_folder_path)
        self.player_name = InputBox(WindowSize.WIDTH / 2 + 125, 100, 150, 26)
        self.pve_button = Button(RGB.BEIGE, WindowSize.WIDTH / 2, 225, 120, 50, text="Play!", border_width=2)

    def draw_text(self):
        title_background_surface = pygame.image.load(self._rel_folder_path + "title-paper.png")
        title_background_surface = pygame.transform.scale(title_background_surface, (440, 90))
        title_background_rect = title_background_surface.get_rect(
            center=(WindowSize.WIDTH / 2 - 200, 100)
        )
        self._master.blit(title_background_surface, title_background_rect)

        first_player_surface = self._fonts.BIG_TEXT.render("Your player name: ", True, RGB.BLACK)
        first_player_rect = first_player_surface.get_rect(
            center=(WindowSize.WIDTH / 2 - 200, 100)
        )
        self._master.blit(first_player_surface, first_player_rect)

    def draw_input_boxes(self):
        self.player_name.draw(self._master, self._fonts)

    def draw_buttons(self):
        self.pve_button.draw(self._master, self._fonts)

    def display_error(self, error_msg):
        title_background_surface = pygame.image.load(self._rel_folder_path + "title-paper.png")
        title_background_surface = pygame.transform.scale(title_background_surface, (700, 90))
        title_background_rect = title_background_surface.get_rect(center=(WindowSize.WIDTH / 2, WindowSize.HEIGHT - 65))
        self._master.blit(title_background_surface, title_background_rect)

        title_surface = self._fonts.BIG_TEXT.render(error_msg, True, RGB.RED)
        title_rect = title_surface.get_rect(center=(WindowSize.WIDTH / 2, WindowSize.HEIGHT - 65))
        self._master.blit(title_surface, title_rect)


class InGameMenu(Menu):
    def __init__(self, master, fonts, rel_folder_path, game_controller, board):
        super().__init__(master, fonts, rel_folder_path)
        self.__game_controller = game_controller
        self.__board = board

        self.roll_button = Button(RGB.BEIGE, 500, 10, 125, 50, "Roll dice!", border_width=2)
        self.skip_button = Button(RGB.BEIGE, 650, 10, 125, 50, "Skip", border_width=2)
        self.quit_button = Button(RGB.BEIGE, 800, 10, 125, 50, "Quit", border_width=2)

        self.selected_piece = None
        self.all_pieces = []
        self.state = "roll_dice"

        self.move_piece_rect = None

    def draw_board(self):
        ratio = 0.55

        board_surface = pygame.image.load(self._rel_folder_path + "board.png")
        board_surface = pygame.transform.scale(board_surface, (int(801 * ratio), int(310 * ratio)))
        board_rect = board_surface.get_rect(midleft=(75, WindowSize.HEIGHT / 2))
        self._master.blit(board_surface, board_rect)

    def draw_roll_button(self):
        self.roll_button.draw(self._master, self._fonts)

    def draw_quit_button(self):
        self.quit_button.draw(self._master, self._fonts)

    def draw_skip_button(self):
        self.skip_button.draw(self._master, self._fonts)

    def display_players(self):
        player_names_surface = pygame.image.load(self._rel_folder_path + "title-paper.png")
        player_names_surface = pygame.transform.scale(player_names_surface, (150, 75))
        player_names_rect = player_names_surface.get_rect(topleft=(1, 5))

        player1_name = self.__game_controller.get_name_for_player(1)
        if self.__game_controller.current_player == "player1":
            player1_name_surface = self._fonts.SMALL_BOLD_TEXT.render("Player 1: " + player1_name, True, RGB.BLACK)
        else:
            player1_name_surface = self._fonts.SMALL_TEXT.render("Player 1: " + player1_name, True, RGB.BLACK)
        player1_name_rect = player1_name_surface.get_rect(midleft=(30, 30))

        player2_name = self.__game_controller.get_name_for_player(2)
        if self.__game_controller.current_player == "player2":
            player2_name_surface = self._fonts.SMALL_BOLD_TEXT.render("Player 2: " + player2_name, True, RGB.BLACK)
        else:
            player2_name_surface = self._fonts.SMALL_TEXT.render("Player 2: " + player2_name, True, RGB.BLACK)
        player2_name_rect = player2_name_surface.get_rect(midleft=(30, 55))

        player_names_rect.w = max(player_names_rect.w, player1_name_rect.w + 75, player2_name_rect.w + 75)
        player_names_surface = pygame.transform.scale(player_names_surface, (player_names_rect.w, 75))

        self._master.blit(player_names_surface, player_names_rect)
        self._master.blit(player1_name_surface, player1_name_rect)
        self._master.blit(player2_name_surface, player2_name_rect)

    def draw_dice_value(self):
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

        message = the_way_the_universe_treated_the_player + " Your dice value: " + str(self.__game_controller.
                                                                                       rolled_dice_value)

        self.display_message(message, RGB.BLACK)

    def draw_all_pieces(self):
        self.all_pieces = []

        self.__draw_all_pieces_for("player1")
        self.__draw_all_pieces_for("player2")

    def __draw_all_pieces_for(self, player):
        base_position = (117, 110)
        square_size = (51, 51)
        for index in range(1, self.__board.max_index + 1):
            piece_id = player + "_" + str(index)
            offset = self.__board.get_offset_for_piece(piece_id)
            self.__draw_piece(base_position, offset, square_size, player, index)

    def __draw_piece(self, base_position, offset, square_size, player, index):
        piece_image_file_name = "white-piece.png"
        if player == "player2":
            piece_image_file_name = "black-piece.png"
        ratio = 0.15
        piece_x = base_position[0] + offset[0] * square_size[0]
        piece_y = base_position[1] + offset[1] * square_size[1]

        piece_surface = pygame.image.load(self._rel_folder_path + piece_image_file_name)
        piece_surface = pygame.transform.scale(piece_surface, (int(300 * ratio), int(300 * ratio)))
        piece_id = player + "_" + str(index)
        if self.selected_piece is not None and self.selected_piece == piece_id:
            self.__draw_select_square_for(piece_id, (piece_x, piece_y), ratio)
            self.__draw_move_square_for(piece_id, base_position, square_size, ratio)
        piece = PieceRect(piece_surface.get_rect(center=(piece_x, piece_y)), piece_id)
        self._master.blit(piece_surface, piece.rect)

        self.all_pieces.append(piece)

    def __draw_select_square_for(self, piece_id, piece_coordinates, ratio):
        player = piece_id.split("_")[0]
        if player != self.__game_controller.current_player:
            return

        piece_width = 300
        piece_height = 300
        select_square_ratio = ratio * 1.05

        square_dimensions = (piece_width * select_square_ratio, piece_height * select_square_ratio)

        square_rect = pygame.Rect(piece_coordinates, square_dimensions)
        square_rect.center = piece_coordinates
        pygame.draw.rect(self._master, RGB.GOLDEN_YELLOW, square_rect, 5)

    def __draw_move_square_for(self, piece_id, base_position, square_size, ratio):
        piece = self.__game_controller.get_piece_by_id(piece_id)
        if piece.owner != self.__game_controller.current_player:
            return

        piece_width = 300
        piece_height = 300

        select_square_ratio = ratio * 1.05
        square_dimensions = (piece_width * select_square_ratio, piece_height * select_square_ratio)

        new_location = piece.location + self.__game_controller.rolled_dice_value
        try:
            new_offset = self.__board.get_offset(new_location, piece.index, piece.owner)
            piece_x = base_position[0] + new_offset[0] * square_size[0]
            piece_y = base_position[1] + new_offset[1] * square_size[1]
            new_coordinates = (piece_x, piece_y)

            square_rect = pygame.Rect(new_coordinates, square_dimensions)
            square_rect.center = new_coordinates
            pygame.draw.rect(self._master, RGB.BLUE, square_rect, 5)

            self.move_piece_rect = MovePieceRect(square_rect, piece.id)
        except MetaException:
            self.move_piece_rect = None

    def display_error(self, error_msg):
        self.display_message(error_msg, RGB.RED)

    def display_waiting_message(self):
        self.display_message("The computer is making a move, please wait...", RGB.BLACK)

    def display_message(self, message, color):
        title_background_surface = pygame.image.load(self._rel_folder_path + "title-paper.png")
        title_background_surface = pygame.transform.scale(title_background_surface, (900, 65))
        title_background_rect = title_background_surface.get_rect(center=(WindowSize.WIDTH / 2, WindowSize.HEIGHT - 40))
        self._master.blit(title_background_surface, title_background_rect)

        title_surface = self._fonts.SMALL_TEXT.render(message, True, color)
        title_rect = title_surface.get_rect(center=(WindowSize.WIDTH / 2, WindowSize.HEIGHT - 40))
        self._master.blit(title_surface, title_rect)


class WinnerMenu(Menu):
    def __init__(self, master, fonts, rel_folder_path, game_controller):
        super().__init__(master, fonts, rel_folder_path)
        self.__game_controller = game_controller
        self.quit_button = Button(RGB.BEIGE, WindowSize.WIDTH / 2, WindowSize.HEIGHT - 150, 125, 50, "Quit",
                                  border_width=2)

    def draw_winner_message(self):
        if self.__game_controller.winner_name != "computer":
            winner_msg_rows = ["Congratulations, " + self.__game_controller.winner_name + "!",
                               "You have won at the amazing,", "greatest game there is:", "The Royal Game of Ur!"]
        else:
            winner_msg_rows = ["The computer has actually beaten you...",
                               "This must be a dark day for mankind.", "Oh well, good luck next time!",
                               "Hope you enjoyed the greatest game there is,",
                               "The Royal Game of Ur!"
                               ]
        messages = []

        max_width = 550
        y_offset = 0
        for winner_msg in winner_msg_rows:
            winner_msg_surface = self._fonts.MEDIUM_TEXT.render(winner_msg, True, RGB.BLACK)
            winner_msg_rect = winner_msg_surface.get_rect(center=(WindowSize.WIDTH / 2, 150 + y_offset))
            messages.append((winner_msg_surface, winner_msg_rect))

            max_width = max(max_width, winner_msg_rect.w + 150)
            y_offset += 25

        winner_bg_surface = pygame.image.load(self._rel_folder_path + "title-paper.png")
        winner_bg_surface = pygame.transform.scale(winner_bg_surface, (max_width, 350))
        winner_bg_rect = winner_bg_surface.get_rect(midtop=(WindowSize.WIDTH / 2, 50))
        self._master.blit(winner_bg_surface, winner_bg_rect)
        for message in messages:
            self._master.blit(*message)

    def draw_quit_button(self):
        self.quit_button.draw(self._master, self._fonts)
