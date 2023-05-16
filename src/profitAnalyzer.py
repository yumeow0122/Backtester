class AnalyzeData:
    def __init__(self):
        self.win_count = 0
        self.loss_count = 0
        self.win_profit = []
        self.loss_profit = []
        self.asset_change = []

class ProfitAnalyzer:
    def __init__(self):
        pass

    def calculate_total_profit(analyzeData):
        return sum(analyzeData.win_profit) + sum(analyzeData.loss_profit)

    def calculate_win_rate(analyzeData):
        total_trades = analyzeData.win_count + analyzeData.loss_count
        if total_trades > 0:
            return analyzeData.win_count / total_trades
        else:
            return 0.0

    def calculate_profit_factor(analyzeData):
        total_wins = sum(analyzeData.win_profit)
        total_losses = abs(sum(analyzeData.loss_profit))
        if total_losses > 0:
            return total_wins / total_losses
        else:
            return float('inf')  # 若没有亏损交易，则盈亏比为正无穷

    def calculate_average_profit(analyzeData):
        total_profit = sum(analyzeData.win_profit + analyzeData.loss_profit)
        total_trades = analyzeData.win_count + analyzeData.loss_count
        if total_trades > 0:
            return total_profit / total_trades
        else:
            return 0.0
        