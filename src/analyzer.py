import matplotlib.pyplot as plt


class Analyzer:
    def __init__(self):
        pass

    
    def show(self, data, analyze_data, agent_data):
        calculator = Calculator()
        total_profit = calculator.total_profit(analyze_data)
        win_rate = calculator.win_rate(analyze_data)
        profit_factor = calculator.profit_factor(analyze_data)
        
        # print out analyze result
        print(f"Total Trades: {analyze_data.win_count + analyze_data.loss_count}")
        print(f"Win Rate: {win_rate}")
        print(f"Profit Rate: {(total_profit / analyze_data.initial_asset) * 100}%")
        print(f"Profit Factor: {profit_factor}")
        
        # plot the graph
        self.plot_stock_price(analyze_data, data)
        
    def plot_stock_price(self, analyze_data, data):
        # 从价格数据中获取日期和收盘价列
        date = data.index
        close_price = data['Close']

        # 创建绘图
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # 绘制收盘价曲线
        ax1.plot(date, close_price, color='blue')
        ax1.set_ylabel("Close Price", color='blue')
        
        # 创建资产变化的坐标轴
        ax2 = ax1.twinx()
        
        # 从分析数据中获取日期和资产变化列
        asset_change = analyze_data.asset_change
        # 计算资产百分比变化
        asset_percentage_change = [((change / asset_change[0]) - 1) * 100 for change in asset_change]
        
        # 绘制资产变化曲线        
        ax2.plot(date, asset_change, color='red')
        ax2.set_ylabel("Asset Percentage Change", color='red')

        # 设置图表标题和轴标签
        plt.title("Stock Price and Asset Change")
        ax1.set_xlabel("Date")
        plt.savefig('./report/analyze_report.png')
        # 显示图表
        plt.show()

class Calculator:
    def __init__(self):
        pass
    
    def total_profit(self, analyze_data):
        print(sum(analyze_data.win_profit))
        print(sum(analyze_data.loss_profit))
        return round(sum(analyze_data.win_profit) + sum(analyze_data.loss_profit), 4)

    def win_rate(self, analyzeData):
        total_trades = analyzeData.win_count + analyzeData.loss_count
        if total_trades > 0:
            return round(analyzeData.win_count / total_trades, 4)
        else:
            return 0.0

    def profit_factor(self, analyzeData):
        total_wins = sum(analyzeData.win_profit)
        total_losses = abs(sum(analyzeData.loss_profit))
        if total_losses > 0:
            return round(total_wins / total_losses, 4)
        else:
            return float('inf')  # 若没有亏损交易，则盈亏比为正无穷