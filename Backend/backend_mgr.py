import pygame
from Backend.Characters import Player
from Backend.Characters import enemy
from Backend.Characters import Trophy
from Backend.files_data import get_files_data
from Backend.Time import Time


class BackEndManager:

    def __init__(self):
        self.player1 = Player()
        self.enemies = [enemy() for i in range(1)]  #[]
        self.cup = Trophy()
        self._clock = pygame.time.Clock()
        self.time = Time()
        self.reward = 0
        self.SCREEN_WIDTH = 1233
        self.SCREEN_HEIGHT = 640
        self.high_score_file, self.high_score, self.user_name_file, self.user_name = get_files_data()
        self.FPS = 60
        self.frame_iteration = 0
        self.limit = 300
        self.games = 0

    def delay_time(self, n, period):
        i = 0
        while i < n:
            pygame.time.delay(period)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = n + 1
                    pygame.quit()

    def write_on_high_score_file(self, high_score):
        with open(self.high_score_file, 'w', encoding='UTF-8') as file:
            file.write(str(high_score))

    def write_on_user_name_file(self, user_name):
        with open(self.user_name_file, 'w', encoding='UTF-8') as file:
            file.write(user_name)
        self.user_name = user_name

    @property
    def get_high_score(self):
        return self.high_score

    @property
    def get_high_score_user_name(self):
        return self.user_name

    @property
    def get_score_now(self):
        return self.player1.score

    def get_adj_hitboxes(self, num):
        hb1 = (self.player1.x - num, self.player1.y, 31, 42)
        hb2 = (self.player1.x + num, self.player1.y, 31, 42)
        hb3 = (self.player1.x, self.player1.y - num, 31, 42)
        hb4 = (self.player1.x, self.player1.y + num, 31, 42)
        return hb1, hb2, hb3, hb4


    def get_diagonal_hitboxes(self, num):
        hb1 = (self.player1.x - num, self.player1.y - num, 31, 42)
        hb2 = (self.player1.x + num, self.player1.y - num, 31, 42)
        hb3 = (self.player1.x - num, self.player1.y + num, 31, 42)
        hb4 = (self.player1.x + num, self.player1.y + num, 31, 42)
        return hb1, hb2, hb3, hb4


    @property
    def get_player_direction(self):
        return self.player1.direction

    def restart_all(self):
        self.games += 1
        self.time.restart_time()
        for ene in self.enemies:
            ene.restart_position()
        self.player1.restart_position()
        self.cup.restart_position(self.games)
        self.player1.reset_score()
        self.frame_iteration = 0
        self.limit = 300
        if self.games % 150 == 0 and len(self.enemies) < 5:
            self.enemies.append(enemy())


    def is_wall(self, hitbox):
        if hitbox[0] + hitbox[2] >= self.SCREEN_WIDTH or hitbox[0] <= 0:
            return 1

        elif hitbox[1] + hitbox[3] >= self.SCREEN_HEIGHT or hitbox[1] <= 0:
            return 1
        else:
            return 0

    def collapse(self, hitbox):
        for enemy in self.enemies:
            if hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and hitbox[1] + hitbox[3] > \
                    enemy.hitbox[1]:
                if hitbox[0] + hitbox[2] > enemy.hitbox[0] and hitbox[0] < enemy.hitbox[0] + \
                        enemy.hitbox[2]:
                    self.reward = -10
                    return 1

        if hitbox[0] + hitbox[2] >= self.SCREEN_WIDTH or hitbox[0] <= 0:
            self.reward = -10
            return 1

        elif hitbox[1] + hitbox[3] >= self.SCREEN_HEIGHT or hitbox[1] <= 0:
            self.reward = -10
            return 1

        if self.frame_iteration > self.limit:
            self.reward = -10
            return 1

        else:
            self.reward = 0

        return 0

    def game_scenario(self, action):
        self.frame_iteration += 1
        self._clock.tick(self.FPS)
        self.time.start = True
        self.time.move_time()
        ret = self.collapse(self.player1.hitbox)
        if ret == 1:
            self.time.restart_time()
            return self.reward, ret, self.player1.score
        if self.player1.hitbox[1] < self.cup.hitbox[1] + self.cup.hitbox[3] and self.player1.hitbox[1] + self.player1.hitbox[3] > self.cup.hitbox[
            1]:
            if self.player1.hitbox[0] + self.player1.hitbox[2] > self.cup.hitbox[0] and self.player1.hitbox[0] < self.cup.hitbox[0] + self.cup.hitbox[
                2]:
                self.cup.restart_position(self.games)
                self.player1.increase_score()
                self.limit += 50
                self.reward = 10
        for enemy in self.enemies:
            enemy.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.player1.move(action, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        return self.reward, ret, self.player1.score