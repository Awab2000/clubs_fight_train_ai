# clubs_fight_train_ai

### This is an AI controled game the main idea of the game is that the agent reach the cup as many times as possibles, and this is the goal of training.

The game is developed using python and pygame and trained an AI model using a Reinforcement Learning approach with Deep Q-Learning to train the agent and predict the actions, I used pytorch to train the model.

The idea behind Reinforcement Learning is that an agent will learn from the environment by interacting with it and receiving rewards for performing actions.

This approach consists in the interaction between two components: an environment (the game itself) and an agent (the team you choose). The agent collects information about its current state and performs an action accordingly. The environment rewards or punishes the agent based on the performed action. Over time, the agent learns what actions maximize the reward (in our case, what actions lead to reaching the cup and avoiding the enemies).

Reinforcement Learning is a family of algorithms and techniques used for Control (e.g. Robotics, Autonomous driving, etc..) and Decision making.

In Reinforcement Learning, we have two main components: the environment (our game) and the agent (our player.. or actually, the Deep Neural Network that drives our player’s actions).

Every time the agent performs an action, the environment gives a reward to the agent, which can be positive or negative depending on how good the action was from that specific state. The goal of the agent is to learn what actions maximize the reward, given every possible state.

The optimal agent can generalize over the entire state space to always predict the best possible action.. even for those situations that the agent has never seen before!

<div>
<img src="https://github.com/user-attachments/assets/a3daf328-8265-4a42-b41a-7a18a4e68fae" width="500">
</div>

## Watch the following video to know how the agent training looks like

[![Video of the game](https://drive.google.com/file/d/1Tfib75YwAsYI64R6skg8s5h_6zzrsZnP/view?usp=sharing)](https://drive.google.com/file/d/1tbBhCZa89PlMtaVqPRm05CAIg_ib6GDv/view?usp=drive_link)


## How to configure this project for your own uses
I'd encourage you to clone and rename this project to use for your own puposes.

You will need to install the following libraries: pygame, pytorch, numpy.

You can change the model input(the states), also you can play with the actions

Also you can play with the hyperparameters(e.g. Learning rate and Discount rate).
