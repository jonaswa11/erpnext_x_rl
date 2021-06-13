import sys
import numpy as np
import math
import random

import gym
import gym_stock

def simulate():
    env.observation_space.sample()

    episodes = 10
    for episode in range(1, episodes+1):
        state = env.reset()
        done = False
        score = 0 
        
        while not done:
            #env.render()
            action = env.action_space.sample()
            n_state, reward, done, info = env.step(action)
            score+=reward
        print('Episode:{} Score:{} FinalState:{}'.format(episode, score, n_state))


if __name__ == '__main__':
    env = gym.make("StockEnvMultiProduct-v0")
    simulate()