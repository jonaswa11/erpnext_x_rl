# Environment for using the trained model

import requests
import json
import pandas as pd
import random
import numpy as np
import datetime
import time
from datetime import timedelta
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym import Env
from gym.spaces import Dict, Discrete, Box
from sectoken import token, host


    # Function for iterating through the data. Example output: 04/07/1996 -> 11/07/1996
def add_day(date):
    new_date = pd.to_datetime(date, dayfirst=True) + pd.DateOffset(days=7) 
    return new_date.strftime("%Y-%m-%d")


headers = {
    'Authorization': token
}

# Get units in stock by id. Example output: 39.0
def get_units_in_stock(item_id):
    units_in_stock = requests.get(f'http:/{host}:8000/api/method/erpnext.api.get_units_in_stock', params={"item_id": item_id}, headers=headers)
    return float(units_in_stock.json()['message'][0]['unitsinstock'])

# Make Material Request in ERPNext
def post_material_request(material_request):
    material_request = requests.post(f'http://{host}:8000/api/resource/Material Request/', json={"data": data},  headers=headers)

# Get last Material Number to check for new action. Example output: MAT-MR-2021-00011
def get_last_material_request_id():
    id = requests.get(f'http://{host}:8000/api/method/erpnext.api.get_last_material_request_id', headers=headers)
    if not id.json()['message']: 
        return "MAT-MR-2021-00000"
    else:
        return id.json()['message'][0]['name']

# Get Data from Purchase Order. Example output: 60.0
def get_total_qty_by_rl_name(rl_name):
    total_qty = requests.get(f'http://{host}:8000/api/method/erpnext.api.get_total_qty_by_rl_name', params={"rl_name": rl_name}, headers=headers)
    return total_qty.json()

# Get stock entry details. Example output: 10
def get_stock_entry_detail():
    stock_entry_details = requests.get(f'http://{host}:8000/api/method/erpnext.api.get_stock_entry_detail', headers=headers)
    return stock_entry_details.json()

# Create new id for purchase order
def new_id():
    old_id = get_last_material_request_id()
    last_num = int(old_id[-5:])
    last_num += 1
    return "MAT-MR-2021-" + str(last_num).zfill(5)

# prefilled data for the material request
data = {
    "idx": 0,
    "docstatus": 1,
    "naming_series": "MAT-MR-.YYYY.-",
    "material_request_type": "Purchase",
    "status": "Draft",
    "company": "MyCompany",
    "set_warehouse": "All Warehouses - MC",
    "doctype": "Material Request",  
}



class StockEnv(gym.Env):
    def __init__(self):

        # number of products we want to track
        self.num_of_products = 3
        
        # index for database
        self.current_rl_name = ""
        
        # Action Space
        self.action_space = Box(low=-1, high=1, shape=(self.num_of_products,), dtype=np.int32)

        # Observation Space
        self.observation_space = Box(low=0, high=self.num_of_products * 400, shape=(self.num_of_products, ), dtype=np.float32)

        # Set start stock
        self.state = np.array([])
        for products in range(self.num_of_products):
            units_in_stock = get_units_in_stock(products + 1)
            self.state = np.append(self.state, units_in_stock)

        # Get data on stock in ERPNext
        all_entries = get_stock_entry_detail()

        for entry in all_entries['message']:
            self.state[int(entry['item_code']) - 1] += int(entry['qty'])

        
    def step(self, action):
        
        all_entries = get_stock_entry_detail()

        for entry in all_entries['message']:
            self.state[int(entry['item_code']) - 1] += int(entry['qty'])
        
        # Apply action

        action += 1
        action *= 10
        action = np.round(action, 0)

        name = new_id()
        self.current_rl_name = name
        transaction_date = datetime.datetime.now().strftime("%Y-%m-%d")
        data['name'] = name
        data['rl_name'] = name
        data['transaction_date'] = transaction_date
        data['schedule_date'] = add_day(transaction_date)
        
        
        action_sum = np.sum(action)
        items = []
        i = 0
        for action in action:
            i += 1
            if action == 0:
                pass
            else:               

                item = {
                    "parentfield": "items",
                    "parenttype": "Material Request",
                    "stock_uom": "Nos",
                    "warehouse": "Stores - MC",
                    "uom": "Nos",
                    "cost_center": "Main - MC",
                    "expense_account": "Cost of Goods Sold - MC",
                    "doctype": "Material Request Item"
                }
                item['parent'] = name
                item['item_code'] = int(i)
                item['schedule_date'] = add_day(transaction_date)
                item['qty'] = int(action)
                items.insert(i, item)
        
        
        data['items'] = items

        # make material request in ERPNext
        post_material_request(json.dumps(data))

        if  action_sum != 0:
            available = True
            while available == True:
                total_qty = get_total_qty_by_rl_name(self.current_rl_name)
                if not total_qty['message']:
                    time.sleep(10)
                else:
                    available = False


            total_qty = float(total_qty['message'][0]['total_qty'])
        
            reward = (total_qty - action_sum) / 10
            
            print(reward)
        else:
            reward = 0
        
        # cooldown
        for x in range(10):
            print("Waiting ..." , "[", x, "/10]")
            time.sleep(10)

  
        done = False

        
        # Set placeholder for info
        info = {}

        # Return step information
        return self.state, reward, done, info


    def reset(self):

        self.current_rl_name = ""
        items = []      
        return self.state.astype(np.float32)



    def render(self, mode='console'):
        if mode != 'console':
            raise NotImplementedError()
        print("Stock", self.state)
        print("Date", self.current_date)

    def close(self):
        pass

