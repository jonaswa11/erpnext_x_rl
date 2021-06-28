# environment for training a model

import requests
import json
import pandas as pd
import random
import numpy as np

from datetime import datetime, timedelta
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym import Env
from gym.spaces import Dict, Discrete, Box, Tuple



    # Function for iterating through the data. Example output: 04/07/1996 -> 11/07/1996
def add_day(date):
    new_date = pd.to_datetime(date, dayfirst=True) + pd.DateOffset(days=1) 
    return new_date.strftime("%d.%m.%Y")

    # Add or subtract days from date to prevent overfitting. Example output: 04/07/1996 -> 05/07/1996
def add_day_random(date):
    new_date = pd.to_datetime(date, dayfirst=True) + pd.DateOffset(days=np.random.randint(-2,2)) 
    return new_date.strftime("%d.%m.%Y")


class StockEnvMultiProduct(gym.Env):
    def __init__(self):
        
        # Set start values 
        self.df = pd.read_csv('~/../../home/ubuntu/rltest/gym-stock/gym_stock/dataset/pandasdata.csv')
        self.df['OrderDate'] = self.df['OrderDate'].apply(lambda x: add_day_random(x))
        self.episodes = 0
        self.timesteps = 0
        self.num_of_products = 3
        self.neg_buy_reward = 0
        self.stock_reward = 0
       

 
        # Actions Space
        self.action_space = Box(low=-1, high=1, shape=(self.num_of_products,), dtype=np.int32)

        # Observation Space
        self.observation_space = Box(low=0, high=self.num_of_products * 400, shape=(self.num_of_products, ), dtype=np.float32)

        # Set random start stock       
        self.state = np.array(np.random.randint(20, 200, size=(self.num_of_products)))
        
        # Set simulation end date 
        self.current_date = "04.07.1996"
        self.end_date = "06.05.1998"  
        
    def step(self, action):

        # Apply action
        action += 1
        action *= 10
        action = np.round(action, -1)

        #calculate reward
        self.neg_buy_reward = np.sum(action) / (self.num_of_products * 10)
        self.state = np.add(self.state, action)
        self.timesteps += 1
        
        # One step
        list = (self.df.loc[(self.df['OrderDate'] == self.current_date)])

        if list.empty:
            pass   
        else: 
            for i in range(0, len(list)): 
                index = list.iloc[i]['ProductID'].astype(int)
                if  index > self.num_of_products:
                    pass
                else:
                    self.state[index - 1] -= list.iloc[i]['Quantity'] * (round(random.uniform(0.5,1.5), 1))
    
        # Reduce simulation length value at each step by 1 
        self.current_date = add_day(self.current_date)
        
        
        # Return reward
        if not (self.state > 0).all() or not (self.state < 400).all(): 
            reward = - 1 * (self.num_of_products * 80)
        else:
            reward = 1 - self.neg_buy_reward


        # Check if simulation is done
        if self.current_date == self.end_date or not (self.state > 0).all() or not (self.state < 400).all(): 
            done = True
        else:
            done = False
        
        # Set placeholder for info
        info = {}

        # Return step information
        return self.state, reward, done, info


    def reset(self):
        #value for randomizing date after each episode to prevent overfitting
        self.episodes += 1
        if(self.episodes % 1 == 0):            
            self.df = pd.read_csv('~/../../home/ubuntu/rltest/gym-stock/gym_stock/dataset/pandasdata4.csv')
            self.df['OrderDate'] = self.df['OrderDate'].apply(lambda x: add_day_random(x))
        # Reset stock
        self.state = np.array(np.random.randint(20, 200, size=(self.num_of_products)))
        # Reset simulation length counter
        self.current_date = "04.07.1996"
        self.timesteps = 0
        self.neg_buy_reward = 0
        
        return self.state.astype(np.float32)



    def render(self, mode='console'):
        if mode != 'console':
            raise NotImplementedError()
        print("Stock", self.state)
        print("Date", self.current_date)

    def close(self):
        pass

