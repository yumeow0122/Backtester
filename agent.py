import os
from dotenv import load_dotenv
from binance import Client

from src.data_controller import DataController

load_dotenv()
client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))

class Agent:
    def __init__(self):
        self.data = None
        pass
        
    def get_data(self, symbol, interval, look_back):
        print( symbol, interval, look_back)
        data = DataController.get_data(client, symbol, interval, look_back)
        return data
    
    def set_data(self, data):
        self.data = data
