
import pygame
from src.ui.colors import RGB
from src.ui.fonts import Font


class Button:
    def __init__(self, bg_color, x, y, width, height, text='', text_color=RGB.WHITE, border_color=RGB.BLACK,
                 border_width=0, active=True):
        self.__bg_color = bg_color
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__text = text
        self.__text_color = text_color
        self.__border_color = border_color
        self.__border_width = border_width
        self.__active = active

        self.__hover_amount = 0
        self.__rect = pygame.Rect(0, 0, self.__width, self.__height)

    def draw(self, master, fonts: Font):
        border_radius = 2
        if self.__border_width != 0:
            border_rect = pygame.Rect((0, 0),
                                      (self.__width + self.__border_width * 2, self.__height + self.__border_width * 2)
                                      )
            border_rect.center = (self.__x, self.__y + self.__height/2 + self.__hover_amount)
            pygame.draw.rect(master,
                             self.__border_color,
                             border_rect,
                             border_radius=border_radius
                             )

        self.__rect = main_rect = pygame.Rect(0, 0, self.__width, self.__height)
        main_rect.midtop = (self.__x, self.__y + self.__hover_amount)
        pygame.draw.rect(master,
                         self.__bg_color,
                         main_rect,
                         border_radius=border_radius
                         )

        if not self.__text == '':
            text_surface = fonts.MEDIUM_TEXT.render(self.__text, True, self.__text_color)
            text_rect = text_surface.get_rect()
            text_rect.center = (self.__x, self.__y + self.__height / 2 + self.__hover_amount)
            master.blit(text_surface, text_rect)

    def mouse_is_over(self, mouse_pos):
        """
        Preferable, it automatically checks for you the anchor of the rectangle.
        :param mouse_pos: the current location of the mouse
        :return: True if mouse is over the button, False otherwise
        """
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        return self.__rect.collidepoint((mouse_x, mouse_y))

    def mouse_is_over_(self, mouse_pos):
        """
        Not preferable, it depends on the anchor of the rectangle.
        :param mouse_pos: the current location of the mouse
        :return: True if mouse is over the button, False otherwise
        """
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        mouse_is_on_x = self.__x - self.__width / 2 < mouse_x < self.__x + self.__width / 2
        mouse_is_on_y = self.__y < mouse_y < self.__y + self.__height
        if mouse_is_on_x and mouse_is_on_y:
            return True
        return False

    def hover_animation(self):
        if self.__active:
            self.__hover_amount = 10

    def stop_hovering(self):
        self.__hover_amount = 0


class PieceRect:
    def __init__(self, rect, id_):
        self.__rect = rect
        self.__id = id_
        self.selected = False

    @property
    def rect(self):
        return self.__rect

    @property
    def id(self):
        return self.__id

    def mouse_is_over(self, mouse_pos):
        """
        Preferable, it automatically checks for you the anchor of the rectangle.
        :param mouse_pos: the current location of the mouse
        :return: True if mouse is over the button, False otherwise
        """
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        return self.rect.collidepoint((mouse_x, mouse_y))


class MovePieceRect:
    def __init__(self, rect, piece_id):
        self.__rect = rect
        self.__piece_id = piece_id

    @property
    def rect(self):
        return self.__rect

    @property
    def piece_number(self):
        return self.__piece_id.split("_")[1]

    def mouse_is_over(self, mouse_pos):
        """
        Preferable, it automatically checks for you the anchor of the rectangle.
        :param mouse_pos: the current location of the mouse
        :return: True if mouse is over the button, False otherwise
        """
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        return self.rect.collidepoint((mouse_x, mouse_y))
