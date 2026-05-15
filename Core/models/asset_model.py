# 데이터만 담는다

class AssetModel:
    def __init__(self, total_asset=0, profit_loss=0, profit_rate=0, stocks=None):
        self.total_asset = total_asset
        self.profit_loss = profit_loss
        self.profit_rate = profit_rate
        self.stocks = stocks or []