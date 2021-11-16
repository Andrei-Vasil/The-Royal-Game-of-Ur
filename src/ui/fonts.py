import pygame


class Font:
    def __init__(self, rel_folder_path):
        self.TITLE = pygame.font.Font(rel_folder_path + "fonts/Helvetica-Bold.ttf", 48)
        self.BIG_TEXT = pygame.font.Font(rel_folder_path + "fonts/Helvetica.ttf", 32)
        self.MEDIUM_TEXT = pygame.font.Font(rel_folder_path + "fonts/Helvetica.ttf", 24)
        self.SMALL_TEXT = pygame.font.Font(rel_folder_path + "fonts/Helvetica.ttf", 16)
        self.SMALL_BOLD_TEXT = pygame.font.Font(rel_folder_path + "fonts/Helvetica-Bold.ttf", 16)
