
import pygame
from src.ui.colors import RGB
from src.ui.fonts import Font


class InputBox:
    def __init__(self, x, y, width, height, bg_color=RGB.WHITE, text='', active_color=RGB.BLACK,
                 inactive_color=RGB.DARKGREY, border_color=RGB.BLACK, border_width=0):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__bg_color = bg_color
        self.__text = text
        self.__active_color = active_color
        self.__inactive_color = inactive_color
        self.__border_color = border_color
        self.__border_width = border_width

        self.__active = False
        self.__rect = None

    def becomes_active(self):
        self.__active = True

    def becomes_inactive(self):
        self.__active = False

    @property
    def is_active(self):
        return self.__active

    @property
    def text(self):
        return self.__text

    def draw(self, master, fonts: Font):
        border_radius = 0
        border_rect = None
        if self.__border_width != 0:
            border_rect = pygame.Rect((0, 0),
                                      (self.__width + self.__border_width * 2, self.__height + self.__border_width * 2)
                                      )
            border_rect.midleft = (self.__x - self.__width / 2, self.__y)

        self.__rect = main_rect = pygame.Rect(0, 0, self.__width, self.__height)
        main_rect.midleft = (self.__x - self.__width / 2, self.__y)

        text_color = self.__active_color
        if not self.__active:
            text_color = self.__inactive_color

        text_rect = text_surface = None
        if not self.__text == '':
            text_surface = fonts.SMALL_TEXT.render(self.__text, True, text_color)
            text_rect = text_surface.get_rect()
            text_rect.midleft = (self.__x - self.__width / 2 + 5, self.__y)

        if text_rect is not None:
            if border_rect is not None:
                border_rect.w = max(self.__width + self.__border_width * 2, text_rect.w + self.__border_width * 2 + 15)
            main_rect.w = max(self.__width + self.__border_width * 2, text_rect.w + self.__border_width * 2 + 15)

        if border_rect is not None:
            pygame.draw.rect(master,
                             self.__border_color,
                             border_rect,
                             border_radius=border_radius
                             )

        pygame.draw.rect(master,
                         self.__bg_color,
                         main_rect,
                         border_radius=border_radius
                         )

        if text_rect is not None:
            master.blit(text_surface, text_rect)

    def get_input(self, event):
        allowed_chars = " '-0123456789"
        if event.key == pygame.K_BACKSPACE:
            self.__text = self.__text[:-1]
            return
        if len(self.__text) > 25:
            return
        if not ('A' <= event.unicode <= 'Z' or 'a' <= event.unicode <= 'z' or event.unicode in allowed_chars):
            return
        self.__text += event.unicode

    def mouse_is_over(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        return self.__rect.collidepoint((mouse_x, mouse_y))
