import random
from abc import ABC, abstractmethod
import pygame
from pygame.locals import *
from enum import Enum
import numpy as np


class Direction(Enum):
    # STAND = 0
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Character(ABC):

    @abstractmethod
    def get_position(self):
        pass


class Player(Character):
    def __init__(self,x = 1190, y = 50, width = 31, height = 42):   # 1202, 50
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 16
        self.score = 0
        self.direction = Direction.DOWN
        self.hitbox = (self.x , self.y, self.width, self.height)

    def get_position(self):
        return self.x, self.y

    def move(self, action, SCREEN_WIDTH, SCREEN_HEIGHT):

        dirs = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        self.direction = dirs[np.argmax(action)]


        self._move(SCREEN_WIDTH, SCREEN_HEIGHT)


    def _move(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        if self.direction == Direction.LEFT:
            self.x -= self.vel
        elif self.direction == Direction.RIGHT :
            self.x += self.vel
        elif self.direction == Direction.DOWN:
            self.y += self.vel
        elif self.direction == Direction.UP:
            self.y -= self.vel

        self.hitbox = (self.x, self.y, self.width, self.height)

    def restart_position(self):
        # self.x = 1190   # 1202
        # self.y = 50
        self.x = random.randint(50,1190)
        self.y = random.randint(50, 580)
        self.direction = Direction.DOWN
        self.hitbox = (self.x, self.y, self.width, self.height)

    def is_high_score(self, high_score):
        return self.score > high_score

    def increase_score(self):
        self.score += 1

    def reset_score(self):
        self.score = 0


class enemy(Character):
    def __init__(self, width = 31, height = 42):
        self.x = random.randint(200,1000)
        self.y = random.randint(200,500)
        self.width = width
        self.height = height
        self.speedx = 8
        self.speedy = 8
        self.hitbox = (self.x, self.y, self.width, self.height)


    def get_position(self):
        return self.x, self.y

    def move(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.x += self.speedx
        self.y += self.speedy
        if self.x <= 0 or self.x + self.width >= SCREEN_WIDTH:
            self.speedx = - self.speedx
        if self.y <= 0 or self.y + self.height >= SCREEN_HEIGHT:
            self.speedy = -self.speedy

        self.hitbox = (self.x, self.y, self.width, self.height)

    def restart_position(self):
        self.x = random.randint(200,1000)
        self.y = random.randint(200,500)
        self.hitbox = (self.x, self.y, self.width, self.height)


class Trophy(Character):
    def __init__(self, x = 0, y = 0, width = 31, height = 53):
        self.x = random.randint(1001, 1180)   # 0, 1200
        self.y = random.randint(20, 570)    # 0,585
        self.height = height
        self.width = width
        self.hitbox = (self.x, self.y, self.width, self.height)


    def get_position(self):
        return self.x, self.y


    def restart_position(self, games):
        # if 1 <= games <= 100:
        #     self.x = random.randint(1001, 1180)
        #     self.y = random.randint(20, 570)
        # elif 101 <= games <= 200:
        #     self.x = random.randint(801, 1180)
        #     self.y = random.randint(20, 570)
        # elif 201 <= games <= 300:
        #     self.x =random.randint(601, 1180)
        #     self.y = random.randint(20, 570)
        # elif 301 <= games <= 400:
        #     self.x = random.randint(401,1180)
        #     self.y = random.randint(20, 570)
        # elif 401 <= games <= 500:
        #     self.x = random.randint(201,1180)
        #     self.y = random.randint(20, 570)
        # elif 501 <= games:
        self.x = random.randint(40,1180)  # 0, 1200
        self.y = random.randint(20,570)    # 0,585
        self.hitbox = (self.x, self.y, self.width, self.height)
