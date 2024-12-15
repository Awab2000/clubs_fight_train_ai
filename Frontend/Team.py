import pygame
from pygame.locals import *


class Team:
    def __init__(self, logo_image, stad_image, chant, rival_image, pos_x, pos_y, rival_pos_x, rival_pos_y, is_turn = False, width = 31, height = 42):
        self.logo_image = pygame.image.load(logo_image)
        self.stad_image = pygame.image.load(stad_image)
        self.chant = chant
        self.rival_image = pygame.image.load(rival_image)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rival_pos_x = rival_pos_x
        self.rival_pos_y = rival_pos_y
        self.is_turn = is_turn
        self.width = width
        self.height = height
        self.display = None

    def draw_logo(self):
        self.display.blit(self.logo_image, (self.pos_x, self.pos_y))

    def draw_stad(self):
        self.display.blit(self.stad_image, (0, 0))


    def play_chant(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.chant)
        pygame.mixer.music.play(-1)

    def draw_rival(self):
        self.display.blit(self.rival_image, (self.rival_pos_x, self.rival_pos_y))