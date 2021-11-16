
import pygame
# import PIL
from src.domain.validators import MetaException
from src.ui.fonts import Font
from src.ui.window import Window
from src.ui.menus import MainMenu, OptionsMenu, PVEMenu, InGameMenu, WinnerMenu, PVPMenu


class Clock:
    def __init__(self):
        self.__clock = pygame.time.Clock()

    def limit_fps(self, fps_limit):
        self.__clock.tick(fps_limit)


class GUI:
    def __init__(self, board, game_controller):
        pygame.init()  # init pygame
        pygame.display.quit()  # but close the window

        self.__rel_folder_path = "ui/resources/"
        if __name__ == "__main__":
            self.__rel_folder_path = "resources/"

        self.__window = None
        self.__main_menu = None
        self.__options_menu = None
        self.__pvp_menu = None
        self.__pve_menu = None
        self.__in_game_menu = None
        self.__winner_menu = None
        self.__clock = None
        self.__fps_limit = 90

        self.__ui = "gui"
        self.__done = True
        self.__board = board
        self.__game_controller = game_controller

        self.__fonts = Font(self.__rel_folder_path)

        self.__state = "main_menu"
        self.__state_cases = {"main_menu": self.__print_main_menu,
                              "options": self.__print_options_menu,
                              "pvp_pick_names": self.__print_pvp_menu,
                              "pve_pick_names": self.__print_pve_menu,
                              "in_game": self.__print_in_game_menu,
                              "win": self.__print_win_menu
                              }
        self.__state_events = {"main_menu": self.__main_menu_events,
                               "options": self.__options_menu_events,
                               "pvp_pick_names": self.__pvp_menu_events,
                               "pve_pick_names": self.__pve_menu_events,
                               "in_game": self.__in_game_events,
                               "win": self.__win_events
                               }

        self.__error_msg = None

    # anything that has to do with the screen and events:
    def run(self):
        self.__ui = "gui"
        self.__window = Window(self.__rel_folder_path)
        self.__main_menu = MainMenu(self.__window.main_bg, self.__fonts, self.__rel_folder_path)
        self.__options_menu = OptionsMenu(self.__window.main_bg, self.__fonts, self.__rel_folder_path)
        self.__pvp_menu = PVPMenu(self.__window.main_bg, self.__fonts, self.__rel_folder_path)
        self.__pve_menu = PVEMenu(self.__window.main_bg, self.__fonts, self.__rel_folder_path)
        self.__in_game_menu = InGameMenu(self.__window.main_bg, self.__fonts, self.__rel_folder_path,
                                         self.__game_controller, self.__board)
        self.__winner_menu = WinnerMenu(self.__window.main_bg, self.__fonts, self.__rel_folder_path,
                                        self.__game_controller)

        self.__clock = Clock()

        self.__done = False
        while not self.__done:
            try:
                self.__treat_events()
            except MetaException as ex:
                self.__error_msg = str(ex)

            if self.__done is True or self.__ui == "console":
                self.__window.close()
                break

            self.__update_screen()
            pygame.display.update()

            self.__clock.limit_fps(self.__fps_limit)

        return self.__done, self.__ui

    def __treat_events(self):
        for event in pygame.event.get():
            # noinspection PyArgumentList
            self.__state_events[self.__state](event)
            if event.type == pygame.QUIT:
                self.__done = True

    def __main_menu_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.__main_menu.play_button.mouse_is_over(mouse_pos):
                self.__state = "options"
            if self.__main_menu.switch_ui_button.mouse_is_over(mouse_pos):
                self.__ui = "console"
            if self.__main_menu.quit_button.mouse_is_over(mouse_pos):
                self.__done = True
        if event.type == pygame.MOUSEMOTION:
            if self.__main_menu.play_button.mouse_is_over(mouse_pos):
                self.__main_menu.play_button.hover_animation()
            else:
                self.__main_menu.play_button.stop_hovering()
            if self.__main_menu.switch_ui_button.mouse_is_over(mouse_pos):
                self.__main_menu.switch_ui_button.hover_animation()
            else:
                self.__main_menu.switch_ui_button.stop_hovering()
            if self.__main_menu.quit_button.mouse_is_over(mouse_pos):
                self.__main_menu.quit_button.hover_animation()
            else:
                self.__main_menu.quit_button.stop_hovering()

    def __options_menu_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.__options_menu.pvp_button.mouse_is_over(mouse_pos):
                self.__state = "pvp_pick_names"
            if self.__options_menu.pve_button.mouse_is_over(mouse_pos):
                self.__state = "pve_pick_names"
        if event.type == pygame.MOUSEMOTION:
            if self.__options_menu.pvp_button.mouse_is_over(mouse_pos):
                self.__options_menu.pvp_button.hover_animation()
            else:
                self.__options_menu.pvp_button.stop_hovering()
            if self.__options_menu.pve_button.mouse_is_over(mouse_pos):
                self.__options_menu.pve_button.hover_animation()
            else:
                self.__options_menu.pve_button.stop_hovering()

    def __pvp_menu_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.__pvp_menu.pvp_button.mouse_is_over(mouse_pos):
                self.__game_controller.add_player(self.__pvp_menu.first_player_name.text, 1)
                self.__game_controller.add_player(self.__pvp_menu.second_player_name.text, 2)
                self.__state = "in_game"
                self.__error_msg = None
            if self.__pvp_menu.first_player_name.mouse_is_over(mouse_pos):
                self.__pvp_menu.first_player_name.becomes_active()
            else:
                self.__pvp_menu.first_player_name.becomes_inactive()
            if self.__pvp_menu.second_player_name.mouse_is_over(mouse_pos):
                self.__pvp_menu.second_player_name.becomes_active()
            else:
                self.__pvp_menu.second_player_name.becomes_inactive()
        if event.type == pygame.MOUSEMOTION:
            if self.__pvp_menu.pvp_button.mouse_is_over(mouse_pos):
                self.__pvp_menu.pvp_button.hover_animation()
            else:
                self.__pvp_menu.pvp_button.stop_hovering()
        if event.type == pygame.KEYDOWN:
            if self.__pvp_menu.first_player_name.is_active:
                self.__pvp_menu.first_player_name.get_input(event)
            if self.__pvp_menu.second_player_name.is_active:
                self.__pvp_menu.second_player_name.get_input(event)

    def __pve_menu_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.__pve_menu.pve_button.mouse_is_over(mouse_pos):
                self.__game_controller.add_player(self.__pve_menu.player_name.text, 1)
                self.__game_controller.add_player(None, None, is_human=False)
                self.__state = "in_game"
                self.__error_msg = None
            if self.__pve_menu.player_name.mouse_is_over(mouse_pos):
                self.__pve_menu.player_name.becomes_active()
            else:
                self.__pve_menu.player_name.becomes_inactive()
        if event.type == pygame.MOUSEMOTION:
            if self.__pve_menu.pve_button.mouse_is_over(mouse_pos):
                self.__pve_menu.pve_button.hover_animation()
            else:
                self.__pve_menu.pve_button.stop_hovering()
        if event.type == pygame.KEYDOWN:
            if self.__pve_menu.player_name.is_active:
                self.__pve_menu.player_name.get_input(event)

    def __in_game_events(self, event):
        mouse_pos = pygame.mouse.get_pos()

        # win condition:
        if self.__game_controller.win():
            self.__state = "win"

        # button animations:
        if event.type == pygame.MOUSEMOTION:
            if self.__in_game_menu.roll_button.mouse_is_over(mouse_pos):
                self.__in_game_menu.roll_button.hover_animation()
            else:
                self.__in_game_menu.roll_button.stop_hovering()
            if self.__in_game_menu.quit_button.mouse_is_over(mouse_pos):
                self.__in_game_menu.quit_button.hover_animation()
            else:
                self.__in_game_menu.quit_button.stop_hovering()
            if self.__in_game_menu.skip_button.mouse_is_over(mouse_pos):
                self.__in_game_menu.skip_button.hover_animation()
            else:
                self.__in_game_menu.skip_button.stop_hovering()

        # all types of clicks:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.__in_game_menu.selected_piece = None

            # selecting pieces event:
            for piece in self.__in_game_menu.all_pieces:
                if piece.mouse_is_over(mouse_pos):
                    if self.__in_game_menu.state == "roll_dice":
                        raise MetaException("You can't select a piece before rolling the dice!")
                    self.__error_msg = None

                    self.__in_game_menu.selected_piece = piece.id

            # move event:
            if self.__in_game_menu.move_piece_rect is not None and self.__in_game_menu.move_piece_rect.mouse_is_over(
                    mouse_pos):
                if self.__in_game_menu.state == "roll_dice":
                    raise MetaException("You can't move a piece before rolling the dice!")
                self.__game_controller.move_piece(self.__in_game_menu.move_piece_rect.piece_number)
                self.__in_game_menu.state = "roll_dice"
                self.__in_game_menu.selected_piece = None
                self.__in_game_menu.move_piece_rect = None
                self.__error_msg = None

            # skip button event:
            if self.__in_game_menu.skip_button.mouse_is_over(mouse_pos):
                self.__game_controller.switch_players()
                self.__in_game_menu.state = "roll_dice"
                self.__in_game_menu.selected_piece = None
                self.__in_game_menu.move_piece_rect = None
                self.__error_msg = None

            # roll button event:
            if self.__in_game_menu.roll_button.mouse_is_over(mouse_pos):
                if self.__in_game_menu.state == "select_piece":
                    raise MetaException("You can't roll the dice again! You need to select a piece to move, or skip "
                                        "your turn.")
                self.__game_controller.roll_dice()
                self.__in_game_menu.state = "select_piece"
                self.__error_msg = None

            # quit button event:
            if self.__in_game_menu.quit_button.mouse_is_over(mouse_pos):
                self.__game_controller.reset_all()
                self.__in_game_menu.state = "roll_dice"
                self.__state = "main_menu"
                self.__error_msg = None

    def __win_events(self, event):
        mouse_pos = pygame.mouse.get_pos()

        # quit button event:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.__winner_menu.quit_button.mouse_is_over(mouse_pos):
                self.__game_controller.reset_all()
                self.__state = "main_menu"
                self.__error_msg = None

        # button animations:
        if event.type == pygame.MOUSEMOTION:
            if self.__winner_menu.quit_button.mouse_is_over(mouse_pos):
                self.__winner_menu.quit_button.hover_animation()
            else:
                self.__winner_menu.quit_button.stop_hovering()

    def __update_screen(self):
        self.__window.update()
        self.__treat_state()

    # GAMING STUFF:
    def __treat_state(self):
        self.__state_cases[self.__state]()

    def __print_main_menu(self):
        self.__main_menu.draw_title()
        self.__main_menu.draw_buttons()

    def __print_options_menu(self):
        self.__options_menu.draw_title()
        self.__options_menu.draw_buttons()

    def __print_pvp_menu(self):
        self.__pvp_menu.draw_text()
        self.__pvp_menu.draw_input_boxes()
        self.__pvp_menu.draw_buttons()
        if self.__error_msg is not None:
            self.__pvp_menu.display_error(self.__error_msg)

    def __print_pve_menu(self):
        self.__pve_menu.draw_text()
        self.__pve_menu.draw_input_boxes()
        self.__pve_menu.draw_buttons()
        if self.__error_msg is not None:
            self.__pve_menu.display_error(self.__error_msg)

    def __print_in_game_menu(self):
        self.__in_game_menu.display_players()
        self.__in_game_menu.draw_board()
        self.__in_game_menu.draw_roll_button()
        self.__in_game_menu.draw_quit_button()
        self.__in_game_menu.draw_skip_button()
        self.__in_game_menu.draw_all_pieces()

        if self.__in_game_menu.state == "select_piece":
            self.__in_game_menu.draw_dice_value()

        if self.__error_msg is not None:
            self.__in_game_menu.display_error(self.__error_msg)

        if self.__game_controller.pve and self.__game_controller.current_player == "player2":
            self.__in_game_menu.display_waiting_message()
            pygame.display.update()
            self.__game_controller.ai_makes_a_move()

    def __print_win_menu(self):
        self.__winner_menu.draw_winner_message()
        self.__winner_menu.draw_quit_button()
