class TransacationData:
    def __init__(self, asset, levarage, commission):
        self.asset = asset
        self.levarage = levarage
        self.commission = commission / 100
        self.holding = 0
        
        self.initialAsset = self.asset
        self.entryAsset = 0