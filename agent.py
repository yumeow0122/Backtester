import os
import pandas as pd
from dotenv import load_dotenv
from binance import Client
import matplotlib.pyplot as plt

from src.analyzer import Analyzer
from src.data import AgentData, PriceData, AnalyzeData

load_dotenv()
client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))

class Agent:
    def __init__(self, asset, levarage, commission):
        self.data = None
        self.log = pd.DataFrame(columns=[ 'Time', 'Type', 'Price', 'Quantity'])
        self.agent_data = AgentData(asset, levarage, commission)
        self.analyze_data = AnalyzeData(asset)
        pass
        
        
    def open_long_percent(self, idx, percent):
        quantity = round((self.agent_data.asset * percent) / self.data['Open'][idx], 5)
        self.open_long(idx, quantity)
        
        
    def open_long(self, idx, quantity):
        price = self.data['Open'][idx]
        quantity *= self.agent_data.levarage
        cost = quantity * price * (1 + self.agent_data.commission)
        
        self.analyze_data.open_asset = self.agent_data.asset
        self.agent_data.asset -= cost
        self.agent_data.holding += quantity
        self.log = pd.concat([self.log, pd.DataFrame({'Type': ['open_long'], 'Time': [self.data.index[idx]], 'Price': [price], 'Quantity': [quantity]})])
        
        
    def close_long_percent(self, idx, percent):
        quantity = self.agent_data.holding * percent
        self.close_long(idx, quantity)
        
        
    def close_long(self, idx, quantity):
        price = self.data['Open'][idx]
        gain = quantity * price * (1-self.agent_data.commission)
        self.agent_data.asset += gain
        self.agent_data.holding -= quantity
        self.log = pd.concat([self.log, pd.DataFrame({'Type': ['close_long'], 'Time': [self.data.index[idx]], 'Price': [price], 'Quantity': [quantity]})])
        self.record_trade()


    def open_short_percent(self, idx, percent):
        quantity = round((self.agent_data.asset * percent) / self.data['Open'][idx], 5)
        self.open_long(idx, quantity)
        
        
    def open_short(self, idx, quantity):
        price = self.data['Open'][idx]
        quantity *= self.agent_data.levarage
        cost = quantity * price * (1 + self.agent_data.commission)
        
        self.analyze_data.open_asset = self.agent_data.asset
        self.agent_data.asset += cost
        self.agent_data.holding -= quantity
        self.log = pd.concat([self.log, pd.DataFrame({'Type': ['open_long'], 'Time': [self.data.index[idx]], 'Price': [price], 'Quantity': [quantity]})])
        
        
    def close_short_percent(self, idx, percent):
        quantity = self.agent_data.holding * percent
        self.close_long(idx, quantity)
        
        
    def close_short(self, idx, quantity):
        price = self.data['Open'][idx]
        gain = quantity * price * (1 - self.agent_data.commission)
        self.agent_data.asset -= gain
        self.agent_data.holding += quantity
        self.log = pd.concat([self.log, pd.DataFrame({'Type': ['close_long'], 'Time': [self.data.index[idx]], 'Price': [price], 'Quantity': [quantity]})])
        self.record_trade()
        

    def record(self, idx):
        self.analyze_data.asset_change.append(self.agent_data.asset + self.agent_data.holding * self.data['Close'][idx])
    
    
    def record_trade(self):
        profit = self.agent_data.asset - self.analyze_data.open_asset
        if profit > 0:
            self.analyze_data.win_count += 1
            self.analyze_data.win_profit.append(profit)
        else:
            self.analyze_data.loss_count += 1
            self.analyze_data.loss_profit.append(profit)        

                        
    def use_data(self, symbol, interval, look_back):
        self.data = PriceData.get_data(client, symbol, interval, look_back)
        return self.data
    
    
    
    def terminate(self):
        if(self.agent_data.holding > 0):
            self.close_long(len(self.data)-1, self.agent_data.holding)
            
        # transacation log
        self.log.set_index('Time', inplace=True)
        self.log.to_csv('./report/log.csv')
        analyzer = Analyzer()
        analyzer.show(self.data, self.analyze_data, self.agent_data)