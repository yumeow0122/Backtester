from agent import Agent

agent = Agent()

data = agent.get_data('BTCUSDT', '5m', '1 day')
print(data)