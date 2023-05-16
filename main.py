import talib
from agent import Agent

agent = Agent(100, 1, 0.1)

data = agent.use_data('ETHUSDT', '15m', '1 day')
# 提取收盘价
close_prices = data['Close']

# 使用TA-Lib计算KD指标
k, d = talib.STOCH(close_prices, close_prices, close_prices, fastk_period=9, slowk_period=5, slowd_period=4)

# 进行简单的回测
for i in range(len(data)):
    if k[i] > d[i] and k[i-1] < d[i-1] and agent.transacationData.holding == 0:
        # KD金叉，开多仓
        quantity = agent.transacationData.asset / data['Close'][i]
        agent.open_long_position(data['Close'][i], quantity)
    elif k[i] < d[i] and k[i-1] > d[i-1] and agent.transacationData.holding > 0:
        # KD死叉，平多仓
        agent.close_long_position(data['Close'][i], agent.transacationData.holding)
    agent.analyzeData.asset_change.append(agent.transacationData.asset+agent.transacationData.holding*data['Close'][i])
    #print(agent.transacationData.asset, agent.transacationData.holding, agent.transacationData.asset+agent.transacationData.holding*data['Close'][i])

# 执行分析
agent.analyze()
