
import pygame


class WindowSize:
    WIDTH = 910
    HEIGHT = 422


class Window:
    def __init__(self, rel_folder_path):
        self.__rel_folder_path = rel_folder_path

        self.__init_window()
        self.update()

    def __init_window(self):
        pygame.display.init()
        pygame.display.set_caption("The Royal Game of Ur")
        icon = pygame.image.load(self.__rel_folder_path + "icon.png")
        pygame.display.set_icon(icon)
        self.main_bg = pygame.display.set_mode((WindowSize.WIDTH, WindowSize.HEIGHT))

    def update(self):
        self.__place_background()

    def close(self):
        pygame.display.quit()

    def __place_background(self):
        background_image = pygame.image.load(self.__rel_folder_path + "background.jpg").convert()
        self.main_bg.blit(background_image, (0, 0))
