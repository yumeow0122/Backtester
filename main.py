import talib
from agent import Agent

agent = Agent(100, 1, 0.04)

data = agent.use_data('ETHUSDT', '15m', '31 day')
# 提取收盘价
high, low, open, close = data['High'], data['Low'], data['Open'], data['Close']

# 使用TA-Lib计算KD指标
k, d = talib.STOCH(high, low, close, fastk_period=9, slowk_period=5, slowd_period=4)

# 进行简单的回测
for idx in range(len(data)):
    if k[idx] > d[idx] and k[idx-1] < d[idx-1] and agent.agent_data.holding == 0:
        # KD金叉，开多仓
        agent.open_long_percent(idx, 0.85)
    elif k[idx] < d[idx] and k[idx-1] > d[idx-1] and agent.agent_data.holding > 0:
        # KD死叉，平多仓
        agent.close_long_percent(idx, 1)
    agent.record(idx)

# 执行分析
agent.terminate()