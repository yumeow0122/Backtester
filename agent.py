import os
from dotenv import load_dotenv
from binance import Client
import matplotlib.pyplot as plt

from src.dataFetcher import DataFetcher
from src.transacationData import TransacationData
from src.profitAnalyzer import ProfitAnalyzer, AnalyzeData

load_dotenv()
client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))

class Agent:
    def __init__(self, asset, levarage, commission):        
        self.data = None
        self.analyzeData = AnalyzeData()
        self.transacationData = TransacationData(asset, levarage, commission)
        pass
        
    def open_long_position(self, price, quantity):
        quantity *= self.transacationData.levarage
        cost = quantity * price * (1-self.transacationData.commission)
        
        if cost > self.transacationData.asset:
            print("Insufficient funds to execute the open_long_position.")
        else:
            self.transacationData.entryAsset = self.transacationData.asset
            self.transacationData.asset -= cost
            self.transacationData.holding += quantity

    def close_long_position(self, price, quantity):
        quantity *= self.transacationData.levarage
        cost = quantity * price * (1-self.transacationData.commission)
        
        if self.transacationData.holding < quantity:
            print("Insufficient funds to execute the close_long_position.")
        else:
            self.transacationData.asset += cost
            self.transacationData.holding -= quantity
            
            profit = self.transacationData.entryAsset - self.transacationData.asset
            if profit > 0:
                self.analyzeData.win_count += 1
                self.analyzeData.win_profit.append(profit)
            else:
                self.analyzeData.loss_count += 1
                self.analyzeData.loss_profit.append(profit)
                
    def open_short_position(self, price, quantity):
        quantity *= self.transacationData.levarage
        cost = quantity * price * self.transacationData.commission

        if cost > self.transacationData.asset:
            print("Insufficient funds to execute the open_short_position.")
        else:
            self.transacationData.entryAsset = self.transacationData.asset
            self.transacationData.asset += cost
            self.transacationData.holding -= quantity

    def close_short_position(self, price, quantity):
        quantity *= self.transacationData.levarage
        cost = quantity * price * self.transacationData.commission

        if self.transacationData.holding > -quantity:
            print("Insufficient quantity to execute the close_short_position.")
        else:
            self.transacationData.asset -= cost
            self.transacationData.holding += quantity
        
            profit = self.transacationData.entryAsset - self.transacationData.asset
            if profit > 0:
                self.analyzeData.win_count += 1
                self.analyzeData.win_profit.append(profit)
            else:
                self.analyzeData.loss_count += 1
                self.analyzeData.loss_profit.append(profit)
                
    def use_data(self, symbol, interval, look_back):
        self.data = DataFetcher.get_data(client, symbol, interval, look_back)
        return self.data
    
    def analyze(self):
        totalProfit = ProfitAnalyzer.calculate_total_profit(self.analyzeData)
        winRate = ProfitAnalyzer.calculate_win_rate(self.analyzeData)
        profitFactor = ProfitAnalyzer.calculate_profit_factor(self.analyzeData)
        averageProfit = ProfitAnalyzer.calculate_average_profit(self.analyzeData)
        
        # 在这里可以根据需要进一步处理或输出分析结果
        print(f"Total profit: {totalProfit}")
        print(f"Win rate: {winRate}")
        print(f"Profit factor: {profitFactor}")
        print(f"Average profit: {averageProfit}")
        
        # 绘制股价 K 线图和资产变化图表
        self.plot_stock_price()

    def plot_stock_price(self):
        # 从价格数据中获取日期和收盘价列
        date = self.data.index
        close_price = self.data['Close']

        # 创建绘图
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # 绘制收盘价曲线
        ax1.plot(date, close_price, color='blue')
        ax1.set_ylabel("Close Price", color='blue')
        
        # 创建资产变化的坐标轴
        ax2 = ax1.twinx()
        
        # 从分析数据中获取日期和资产变化列
        asset_change = self.analyzeData.asset_change
        # 计算资产百分比变化
        asset_percentage_change = [((change / asset_change[0]) - 1) * 100 for change in asset_change]
        
        # 绘制资产变化曲线        
        ax2.plot(date, asset_change, color='red')
        ax2.set_ylabel("Asset Percentage Change", color='red')

        # 设置图表标题和轴标签
        plt.title("Stock Price and Asset Change")
        ax1.set_xlabel("Date")
        plt.savefig('analyze_report.png')
        # 显示图表
        plt.show()
