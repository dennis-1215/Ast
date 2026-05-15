from PySide6.QtCore import QObject, Signal

class AssetController(QObject):

    balance_loaded = Signal(bool)

    def __init__(self, service, view):
        super().__init__()

        self.service = service
        self.view = view

        self.is_balance_loaded = False
        self.is_loading = False

    def refresh(self):
        if self.is_loading:
            return

        self.is_loading = True

        try:
            data = self.service.get_asset_data()
            stocks = self.service.get_balance_data()

            print("AssetController : stocks = ", stocks)

            # 실패 허용
            if stocks is None:
                print("[AssetController] 잔고 조회 실패")

                self.is_balance_loaded = False
                self.balance_loaded.emit(False)

                return


            # 성공
            self.update_summary(data)
            self.update_stocks(stocks)

            self.is_balance_loaded = True
            self.balance_loaded.emit(True)

        except Exception as e:

            print(f"[AssetController] refresh 실패: {e}")

            self.is_balance_loaded = False
            self.balance_loaded.emit(False)

        finally:
            self.is_loading = False

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