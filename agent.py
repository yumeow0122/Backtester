import os
from dotenv import load_dotenv
from binance import Client

from src.data_controller import DataController

load_dotenv()
client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))

class Agent:
    def __init__(self, asset, levarage, commission):        
        self.dataController = DataController()        
        self.transacationData = TransacationData(asset, levarage, commission)
        pass
        
    def open_long_position(self, price, quantity):
        quantity *= self.transacationData.leverage
        cost = quantity * price * self.transacationData.commission
        
        if cost > self.transacationData.asset:
            raise ValueError("Insufficient funds to execute the open_long_position.")
        else:
            self.transacationData.asset -= cost
            self.transacationData.holding += quantity

    def close_long_position(self, price, quantity):
        quantity *= self.transacationData.leverage
        cost = quantity * price * self.transacationData.commission
        
        if self.transacationData.holding < quantity:
            raise ValueError("Insufficient funds to execute the close_long_position.")
        else:
            self.transacationData.asset += cost
            self.transacationData.holding -= quantity
                
    def open_short_position(self, price, quantity):
        quantity *= self.transacationData.leverage
        cost = quantity * price * self.transacationData.commission

        if cost > self.transacationData.asset:
            raise ValueError("Insufficient funds to execute the open_short_position.")
        else:
            self.transacationData.asset += cost
            self.transacationData.holding -= quantity

    def close_short_position(self, price, quantity):
        quantity *= self.transacationData.leverage
        cost = quantity * price * self.transacationData.commission

        if self.transacationData.holding > -quantity:
            raise ValueError("Insufficient quantity to execute the close_short_position.")
        else:
            self.transacationData.asset -= cost
            self.transacationData.holding += quantity
        
    def get_data(self, symbol, interval, look_back):
        data = self.dataController.get_data(client, symbol, interval, look_back)
        return data
