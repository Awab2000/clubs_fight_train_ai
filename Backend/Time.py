import pygame
from pygame.locals import *

class Time:

    def __init__(self):
        self.seconds = 60
        self.milliseconds = 0
        self.start = False

    @property
    def get_seconds(self):
        return self.seconds

    def move_time(self):
        if self.start:
            if self.milliseconds >= 1000:
                self.seconds -= 1
                self.milliseconds = 0
            self.milliseconds += 20

    def restart_time(self):
        self.seconds = 60
        self.milliseconds = 0
        self.start = False
