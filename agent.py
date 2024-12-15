import torch
import random
import numpy as np
from collections import deque
from Frontend.front_end_mgr import FrontEndManager
from Backend.Characters import Direction
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0    # randomness
        self.gamma = 0.9      # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft
        self.model = Linear_QNet(12, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, mgr):
        point_l, point_r, point_u, point_d = mgr.backend_mgr.get_adj_hitboxes(40)
        point_ll, point_rr, point_uu, point_dd = mgr.backend_mgr.get_adj_hitboxes(80)
        point_ul, point_ur, point_dl, point_dr = mgr.backend_mgr.get_diagonal_hitboxes(40)
        point_dul, point_dur, point_ddl, point_ddr = mgr.backend_mgr.get_diagonal_hitboxes(80)

        point_lll, point_rrr, point_uuu, point_ddd = mgr.backend_mgr.get_adj_hitboxes(120)
        point_llll, point_rrrr, point_uuuu, point_dddd = mgr.backend_mgr.get_adj_hitboxes(160)
        point_lllll, point_rrrrr, point_uuuuu, point_ddddd = mgr.backend_mgr.get_adj_hitboxes(200)

        point_ddul, point_ddur, point_dddl, point_dddr = mgr.backend_mgr.get_diagonal_hitboxes(120)
        point_dddul, point_dddur, point_ddddl, point_ddddr = mgr.backend_mgr.get_diagonal_hitboxes(160)
        point_ddddul, point_ddddur, point_dddddl, point_dddddr = mgr.backend_mgr.get_diagonal_hitboxes(20)

        dir_l = mgr.backend_mgr.get_player_direction == Direction.LEFT
        dir_r = mgr.backend_mgr.get_player_direction == Direction.RIGHT
        dir_u = mgr.backend_mgr.get_player_direction == Direction.UP
        dir_d = mgr.backend_mgr.get_player_direction == Direction.DOWN
        # dir_s = mgr.backend_mgr.get_player_direction == Direction.STAND

        state = [
            # Danger right
            mgr.backend_mgr.collapse(point_r),

            # Danger up
            mgr.backend_mgr.collapse(point_u),

            # Danger down
            mgr.backend_mgr.collapse(point_d),

            # Danger left
            mgr.backend_mgr.collapse(point_l),

            # # Danger right_right
            # mgr.backend_mgr.collapse(point_rr),
            #
            # # Danger up_up
            # mgr.backend_mgr.collapse(point_uu),
            #
            # # Danger down_down
            # mgr.backend_mgr.collapse(point_dd),
            #
            # # Danger left_left
            # mgr.backend_mgr.collapse(point_ll),
            #
            # # Danger up_left
            # mgr.backend_mgr.collapse(point_ul),
            #
            # # Danger up_right
            # mgr.backend_mgr.collapse(point_ur),
            #
            # # Danger down_left
            # mgr.backend_mgr.collapse(point_dl),
            #
            # # Danger down_right
            # mgr.backend_mgr.collapse(point_dr),
            #
            # # Danger double up_left
            # mgr.backend_mgr.collapse(point_dul),
            #
            # # Danger double up_right
            # mgr.backend_mgr.collapse(point_dur),
            #
            # # Danger double down_left
            # mgr.backend_mgr.collapse(point_ddl),
            #
            # # Danger double down_right
            # mgr.backend_mgr.collapse(point_ddr),
            #
            #
            # mgr.backend_mgr.collapse(point_lll),
            #
            # mgr.backend_mgr.collapse(point_rrr),
            #
            # mgr.backend_mgr.collapse(point_uuu),
            #
            # mgr.backend_mgr.collapse(point_ddd),
            #
            #
            # mgr.backend_mgr.collapse(point_llll),
            #
            # mgr.backend_mgr.collapse(point_rrrr),
            #
            # mgr.backend_mgr.collapse(point_uuuu),
            #
            # mgr.backend_mgr.collapse(point_dddd),
            #
            #
            # mgr.backend_mgr.collapse(point_lllll),
            #
            # mgr.backend_mgr.collapse(point_rrrrr),
            #
            # mgr.backend_mgr.collapse(point_uuuuu),
            #
            # mgr.backend_mgr.collapse(point_ddddd),
            #
            #
            # mgr.backend_mgr.collapse(point_ddul),
            #
            # mgr.backend_mgr.collapse(point_ddur),
            #
            # mgr.backend_mgr.collapse(point_dddl),
            #
            # mgr.backend_mgr.collapse(point_dddr),
            #
            #
            # mgr.backend_mgr.collapse(point_dddul),
            #
            # mgr.backend_mgr.collapse(point_dddur),
            #
            # mgr.backend_mgr.collapse(point_ddddl),
            #
            # mgr.backend_mgr.collapse(point_ddddr),
            #
            #
            # mgr.backend_mgr.collapse(point_ddddul),
            #
            # mgr.backend_mgr.collapse(point_ddddur),
            #
            # mgr.backend_mgr.collapse(point_dddddl),
            #
            # mgr.backend_mgr.collapse(point_dddddr),
            #
            # mgr.backend_mgr.is_wall(point_r),
            #
            # mgr.backend_mgr.is_wall(point_u),
            #
            # mgr.backend_mgr.is_wall(point_d),
            #
            # mgr.backend_mgr.is_wall(point_l),

            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            # dir_s,

            # Cup location
            mgr.backend_mgr.cup.x < mgr.backend_mgr.player1.x,  # cup left
            mgr.backend_mgr.cup.x > mgr.backend_mgr.player1.x,  # cup right
            mgr.backend_mgr.cup.y < mgr.backend_mgr.player1.y,  # cup up
            mgr.backend_mgr.cup.y > mgr.backend_mgr.player1.y,  # cup down
            ]
        return np.array(state, dtype=int)


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, action, reward, next_state, done in mini_sample:
        #     self.trainer.train_step(state, action, reward, next_state, done)  # slower
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 28
    agent = Agent()
    mgr = FrontEndManager()
    mgr.start()

    while True:
        # get old state
        state_old = agent.get_state(mgr)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = mgr.run(final_move)

        state_new = agent.get_state(mgr)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            mgr.backend_mgr.restart_all()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record and len(mgr.backend_mgr.enemies) >= 3:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()