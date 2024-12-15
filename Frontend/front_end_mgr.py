import pygame
from pygame.locals import *

from data_helper import load_data
from Backend.backend_mgr import BackEndManager

class FrontEndManager:

    def __init__(self):
        self.backend_mgr = BackEndManager()
        self.Display = None
        self.SCREEN_WIDTH = 1233
        self.SCREEN_HEIGHT = 640
        self.caption = "CLUBS FIGHT"
        self.time_x_pos = 600
        self.time_y_pos = 0
        self.score_x_pos = 0
        self.score_y_pos = 0
        self.teams, self.background_img, self.cup_img = load_data()
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.SILVER = (192, 192, 192)
        self.BUTTONS_WIDTH = 180
        self.BUTTONS_HEIGHT = 50
        self.user_text = ''

    @staticmethod
    def play_background_sound():
        pygame.mixer.music.stop()
        pygame.mixer.music.load("Frontend/sounds/Crowd Sound.mp3")
        pygame.mixer.music.play(-1)

    @staticmethod
    def check_quit():
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

    def display_background_image(self):
        self.Display.blit(self.background_img, (0, 0))

    def display_image(self, img, pos):
        self.Display.blit(img, pos)

    def write_on_screen(self, font_type, font_size, font_color, message, pos_x, pos_y, take_width=False):
        font = pygame.font.SysFont(font_type, font_size)
        text = font.render(message, 1, font_color)
        if take_width:
            self.Display.blit(text, (616 - (text.get_width() / 2), pos_y))
        else:
            self.Display.blit(text, (pos_x, pos_y))


    def init_screen(self):
        pygame.init()
        pygame.key.set_repeat()
        self.Display = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("CLUBS FIGHT")

    def game_intro(self):
        while True:
            self.display_background_image()
            self.write_on_screen("comicsans", 70, self.WHITE, "CLUBS FIGHT", 616, 150, True)
            pygame.draw.rect(self.Display, self.WHITE, (305, 402, self.BUTTONS_WIDTH, self.BUTTONS_HEIGHT)) # 350 490
            self.write_on_screen("comicsans", 40, self.BLACK, "Play", 360, 395)     # 430, 475
            pygame.draw.rect(self.Display, self.WHITE, (710, 402, self.BUTTONS_WIDTH, self.BUTTONS_HEIGHT))    # 850, 490
            self.write_on_screen("comicsans", 33, self.BLACK, "High Score", 713, 398)       # 860, 485
            self.write_on_screen("comicsans", 22, self.WHITE,
                            "How To Play: Use the arrows to avoid the rival and reach the Champions league cup",
                            172, 574)   #150, 700
            self.check_quit()
            cur = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if 305 + self.BUTTONS_WIDTH > cur[0] > 305 and self.BUTTONS_HEIGHT + 402 > cur[1] > 402:
                pygame.draw.rect(self.Display, self.SILVER, (305, 402, self.BUTTONS_WIDTH, self.BUTTONS_HEIGHT))
                self.write_on_screen("comicsans", 40, self.BLACK, "Play", 360, 395)
                if click[0] == 1:
                    self.backend_mgr.delay_time(50, 5)
                    break
            if 710 + self.BUTTONS_WIDTH > cur[0] > 710 and self.BUTTONS_HEIGHT + 402 > cur[1] > 402:
                pygame.draw.rect(self.Display, self.SILVER, (710, 402, self.BUTTONS_WIDTH, self.BUTTONS_HEIGHT))
                self.write_on_screen("comicsans", 33, self.BLACK, "High Score", 713, 398)
                if click[0] == 1:
                    self.view_high()
            pygame.display.update()

    def choose(self):
        choose = True
        while choose:
            self.display_background_image()
            positions = [(150, 296), (250, 296), (350, 296), (450, 296), (550, 296), (650, 296), (750, 296),
                         (850, 296), (150, 460), (250, 460), (350, 460),
                         (450, 460), (550, 460), (650, 460), (750, 460), (850, 460), (950, 460), (950, 296),
                         (1050, 296), (1050, 460)]      # 300 to 246, 500 to 410

            for idx, team in enumerate(self.teams):
                team.pos_x, team.pos_y = positions[idx]
                team.display = self.Display
                team.draw_logo()
                team.is_turn = False

            self.write_on_screen("comicsans", 50, self.WHITE, "Choose a team to start the game", 170, 90, True)  # 230, 110
            self.check_quit()

            cur = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            for team in self.teams:
                if team.pos_x + team.width > cur[0] > team.pos_x and team.height + team.pos_y > cur[1] > team.pos_y:
                    pygame.draw.rect(self.Display, self.GREEN, (team.pos_x - 3, team.pos_y - 3, team.width + 3, team.height + 3), 2)
                    if click[0] == 1:
                        team.is_turn = True
                        team.play_chant()
                        choose = False
                        self.backend_mgr.delay_time(50, 5)
                        break
            pygame.display.update()

    def view_high(self):
        while True:
            self.display_background_image()
            self.write_on_screen("comicsans", 50, self.WHITE, "HIGH SCORE", 420, 143, True)   #525, 175
            self.write_on_screen("comicsans", 50, self.WHITE, self.backend_mgr.get_high_score_user_name + ': ' + str(self.backend_mgr.get_high_score), 330, 280, True)     # 410, 340
            pygame.draw.rect(self.Display, self.WHITE, (515, 450, self.BUTTONS_WIDTH, self.BUTTONS_HEIGHT))     # 620, 550
            self.write_on_screen("comicsans", 40, self.BLACK, "Back", 560, 445)     #680, 540
            self.check_quit()
            cur = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if 515 + self.BUTTONS_WIDTH > cur[0] > 515 and self.BUTTONS_HEIGHT + 450 > cur[1] > 450:
                pygame.draw.rect(self.Display, self.SILVER, (515, 450, self.BUTTONS_WIDTH, self.BUTTONS_HEIGHT))
                self.write_on_screen("comicsans", 40, self.BLACK, "Back", 560, 445)
                if click[0] == 1:
                    break
            pygame.display.update()


    def entry(self):
        while True:
            self.play_background_sound()
            self.display_background_image()
            self.write_on_screen("comicsans", 45, self.WHITE, "Type your name:", 390, 145, True)    # 490, 175
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    else:
                        self.user_text += event.unicode

            self.write_on_screen("comicsans", 45, self.WHITE, self.user_text, 390, 280, True)
            pygame.draw.rect(self.Display, self.WHITE, (515, 450, self.BUTTONS_WIDTH, self.BUTTONS_HEIGHT))  # 620, 550
            self.write_on_screen("comicsans", 40, self.BLACK, "Save", 560, 445)  # 680, 540

            cur = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if 515 + self.BUTTONS_WIDTH > cur[0] > 515 and self.BUTTONS_HEIGHT + 450 > cur[1] > 450:
                pygame.draw.rect(self.Display, self.SILVER,
                                 (515, 450, self.BUTTONS_WIDTH, self.BUTTONS_HEIGHT))  # 620, 550
                self.write_on_screen("comicsans", 40, self.BLACK, "Save", 560, 445)
                if click[0] == 1:
                    self.backend_mgr.write_on_user_name_file(self.user_text)
                    self.backend_mgr.write_on_high_score_file(self.backend_mgr.get_high_score)
                    break
            pygame.display.update()


    def game_over(self):
        self.write_on_screen("comicsans", 70, self.RED, "GAME OVER", 390, 280, True)
        pygame.display.update()
        self.backend_mgr.delay_time(200, 10)


    def print_high_score(self):
        self.write_on_screen("comicsans", 45, self.GREEN, "New High Score!!!", 390, 450, True)
        pygame.display.update()
        self.backend_mgr.delay_time(200, 10)

    def RedrawGameWindow(self):
        self.Display.fill(self.BLACK)
        for team in self.teams:
            if team.is_turn:
                team.draw_stad()
                break

        for team in self.teams:
            if team.is_turn:
                team.pos_x, team.pos_y = self.backend_mgr.player1.get_position()
                team.draw_logo()
                break

        for team in self.teams:
            if team.is_turn:
                for enemy in self.backend_mgr.enemies:
                    team.rival_pos_x, team.rival_pos_y= enemy.get_position()
                    team.draw_rival()
                break

        self.write_on_screen("comicsans", 45, self.WHITE, f'{self.backend_mgr.time.get_seconds}', self.time_x_pos, self.time_y_pos)
        self.write_on_screen("comicsans", 30, self.WHITE, f'Player1 Score: {self.backend_mgr.get_score_now}', self.score_x_pos,
                             self.score_y_pos)
        self.display_image(self.cup_img,self.backend_mgr.cup.get_position())    # Should i make cup class like team? i don't know

        pygame.display.update()

        self.check_quit()


    def start(self):
        self.init_screen()
        self.user_text = ''
        self.play_background_sound()
        self.game_intro()
        self.choose()
        self.backend_mgr.restart_all()

    def run(self, action):
        self.RedrawGameWindow()
        return self.backend_mgr.game_scenario(action)
