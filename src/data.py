import pandas as pd

UTC_OFFSET = 28800000

class PriceData:
    def __init__(self):
        pass
        
    @staticmethod
    def get_data(client, symbol, interval, look_back):        
        frame = pd.DataFrame(columns=range(6))
        frame = pd.DataFrame(client.futures_historical_klines(symbol, interval, look_back + ' ago UTC'))
        frame = frame.iloc[:, :6]
        frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        frame = frame.set_index('Time')
        frame.index = pd.to_datetime(frame.index+UTC_OFFSET, unit='ms')
        frame = frame.astype(float)
        return frame

    
class AgentData:
    def __init__(self, asset, levarage, commission):
        self.asset = asset
        self.levarage = levarage
        self.commission = commission / 100
        self.holding = 0        

        
class AnalyzeData:
    def __init__(self, asset):
        self.initial_asset = asset
        self.open_asset = 0
        
        self.win_count = 0
        self.loss_count = 0
        self.win_profit = []
        self.loss_profit = []
        self.asset_change = []