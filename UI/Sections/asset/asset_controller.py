#

class AssetController:

    def __init__(self, service, view):
        self.service = service
        self.view = view

    def refresh(self):
        data = self.service.get_asset_data()
        stocks = self.service.get_balance_data()

        self.update_summary(data)
        self.update_stocks(stocks)

    def update_summary(self, data):

        total = data["total_asset"]
        loss = data["profit_loss"]
        rate = data["profit_rate"]

        self.view.set_asset_summary(total)

        if loss > 0:
            text = f"+{rate:.2f}% (↑ ₩{loss:,})"
            style = "background-color:#FEEEEE;color:#F04452; font-weight: bold; padding: 5px, 10px; border-radius: 8px;"
        elif loss < 0:
            text = f"{rate:.2f}% (↓ ₩{abs(loss):,})"
            style = "background-color:#E8F3FF;color:#3182F6; font-weight: bold; padding: 5px, 10px; border-radius: 8px;"
        else:
            text = "0.00% (- ₩0)"
            style = "background-color:#F2F4F6;color:#4E5968; font-weight: bold; padding: 5px, 10px; border-radius: 8px;"

        self.view.set_profit_badge(text, style)

    def update_stocks(self, stocks):
        self.view.set_stocks(stocks)