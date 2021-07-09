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
from gym.spaces import Dict, Discrete, Box, Tuple
from .sectoken import token, host


    # 04/07/1996 -> 11/07/1996
def add_day(date):
    new_date = pd.to_datetime(date, dayfirst=True) + pd.DateOffset(days=7) 
    return new_date.strftime("%Y-%m-%d")

    # 04/07/1996 -> 05/07/1996
def add_day_random(date):
    new_date = pd.to_datetime(date, dayfirst=True) + pd.DateOffset(days=np.random.randint(-2,2)) 
    return new_date.strftime("%Y-%m-%d")

headers = {
    'Authorization': token
}
# 39.0
def get_units_in_stock(item_id):
    units_in_stock = requests.get(f'http://{host}:8000/api/method/erpnext.api.get_units_in_stock', params={"item_id": item_id}, headers=headers)
    return float(units_in_stock.json()['message'][0]['unitsinstock'])


def post_material_request(material_request):
    material_request = requests.post(f'http://{host}:8000/api/resource/Material Request/', json={"data": data},  headers=headers)

# MAT-MR-2021-00011
def get_last_material_request_id():
    id = requests.get(f'http://{host}:8000/api/method/erpnext.api.get_last_material_request_id', headers=headers)
    if not id.json()['message']: 
        return "MAT-MR-2021-00000"
    else:
        return id.json()['message'][0]['name']

# 60.0
def get_total_qty_by_rl_name(rl_name):
    total_qty = requests.get(f'http://{host}:8000/api/method/erpnext.api.get_total_qty_by_rl_name', params={"rl_name": rl_name}, headers=headers)
    return total_qty.json()

def get_stock_entry_detail():
    stock_entry_details = requests.get(f'http://{host}:8000/api/method/erpnext.api.get_stock_entry_detail', headers=headers)
    return stock_entry_details.json()

def get_purchase_order_items():
    purchase_order_items = requests.get(f'http://{host}:8000/api/method/erpnext.api.get_purchase_order_items', headers=headers)
    return purchase_order_items.json()

def new_id():
    old_id = get_last_material_request_id()
    last_num = int(old_id[-5:])
    last_num += 1
    return "MAT-MR-2021-" + str(last_num).zfill(5)


data = {
    "idx": 0,
    "docstatus": 1,
    "naming_series": "MAT-MR-.YYYY.-",
    "material_request_type": "Purchase",
    "status": "Pending",
    "company": "MyCompany",
    "set_warehouse": "All Warehouses - MC",
    "doctype": "Material Request",  
}




class StockEnv(gym.Env):
    def __init__(self):

        self.num_of_products = 3
        self.current_rl_name = ""
        # Actions we can take: 'don't buy', 'buy', für jedes Produkt
        self.action_space = Box(low=-1, high=1, shape=(self.num_of_products,), dtype=np.int32)

        # Stock array
        self.observation_space = Box(low=0, high=400, shape=(self.num_of_products, ), dtype=np.float32)

        # Set start stock

        self.state = np.array([])
        for products in range(self.num_of_products):
            units_in_stock = get_units_in_stock(products + 1)
            self.state = np.append(self.state, units_in_stock)
        
              
    def step(self, action):

        self.state = np.array([])
        for products in range(self.num_of_products):
            units_in_stock = get_units_in_stock(products + 1)
            self.state = np.append(self.state, units_in_stock)

        # Get data on stock in ERPNext
        orders = get_purchase_order_items()
        for item in orders['message']:
            self.state[int(item['item_code']) - 1] += int(item['qty'])


        # Apply action
        # 0 += 0 
        # 1 += 20  
        # 2 += 40
        print("STATE: ",self.state)
        action += 1
        action *= 10
        action = np.round(action, 0)
        # self.state = np.add(self.state, action)
        print("ACTION: ",action)

        


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
            
            print("REWARD: ", reward)
        else:
            reward = 0
        

        for x in range(2):
            print("Waiting ..." , "[", x, "/3]")
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

