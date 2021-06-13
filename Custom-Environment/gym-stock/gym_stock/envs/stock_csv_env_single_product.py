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
from gym.spaces import Discrete, Box


df = pd.read_csv('~/../../home/ubuntu/rltest/gym-stock/gym_stock/dataset/pandasdata.csv')

    # 07/04/1996 -> 07/05/1996
def add_day(date):
    new_date = pd.to_datetime(date) + pd.DateOffset(days=1) 
    return new_date.strftime("%m/%d/%Y")

class StockEnvSingleProduct(gym.Env):
    def __init__(self):
        
        # Actions we can take: 'don't buy', 'buy', für jedes Produkt
        self.action_space = Discrete(6)
        
        # Stock array    
        self.observation_space = Box(low=np.array([0]), high=np.array([1000]))


        self.total_stock = 3000
        # Set start stock 
        self.state = 50
        
        # Set simulation end date 
        self.current_date = "07/4/1996"
        self.end_date = "10/28/1997"     
        
    def step(self, action):
        
        # Apply action
        # 0 += 0 
        # 1 += 50  
        self.state += action * 10
        
        

         # One step
        list = (df.loc[(df['OrderDate'] == self.current_date)])

        if list.empty:
            pass   
        else: 
            for i in range(0, len(list)):
                if list.iloc[i]['ProductID'] < 12:
                    self.state -= list.iloc[i]['Quantity']
                else: 
                    pass
        
        
        # Reduce simulation length value at each step by 1 
        self.current_date = add_day(self.current_date)
        
        # Calculate reward -> je weniger Lagerkapazität gebraucht wird, desto besser
        if self.state <= 0: 
            reward = -10
        else:
            reward = 1 - 1.001**(self.state)
        
        # Check if done
        if self.current_date == self.end_date or self.state <= 0: 
            done = True
        else:
            done = False
        
        # Set placeholder for info
        info = {}
        
        # Return step information
        return np.array([self.state]).astype(np.float32), reward, done, info

    def reset(self):
        # Reset stock
        self.state = 50
        # Reset simulation length counter
        self.current_date = "07/4/1996"
        return np.array([self.state]).astype(np.float32)



    def render(self, mode='console'):
        if mode != 'console':
            raise NotImplementedError()
        print("Stock", self.state)
        print("Date", self.current_date)

    def close(self):
        pass

