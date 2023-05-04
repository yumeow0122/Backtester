import pandas as pd

UTC_OFFSET = 28800000
class DataFetcher:
    def __init__(self):
        self.data = None
        
    def get_data(client, symbol, interval, look_back):        
        frame = pd.DataFrame(columns=range(6))
        frame = pd.DataFrame(client.futures_historical_klines(symbol, interval, look_back + ' ago UTC'))
        frame = frame.iloc[:, :6]
        frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        frame = frame.set_index('Time')
        frame.index = pd.to_datetime(frame.index+UTC_OFFSET, unit='ms')
        frame = frame.astype(float)
        return frame
    
    