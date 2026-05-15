
class AssetService:
    def __init__(self, api):
        self.api = api

    def get_asset_data(self):
        asset_status = self.api.get_asset_status()

        if asset_status:
            total_asset = int(asset_status[0].get('tot_evlu_amt', 0))  # 총 평가 금액
            profit_loss = int(asset_status[0].get('evlu_pfls_smtl_amt', 0))  # 평가 손익 금액

            # 수익률 계산 (총 평가 금액 - 평가 손익 = 투자 원금)
            principal = total_asset - profit_loss
            profit_rate = (profit_loss / principal * 100) if principal > 0 else 0

            return {
                "total_asset": total_asset,
                "profit_loss": profit_loss,
                "profit_rate": profit_rate
            }

        else:
            return {
                "total_asset": 0,
                "profit_loss": 0,
                "profit_rate": 0
            }

    def get_balance_data(self):
        balance = self.api.get_balance()
        stock = []
        if balance:
            for item in balance:
                code = item.get('pdno', "")                    # 종목코드
                name = item.get('prdt_name', '알수없음')        # 종목명
                qty = item.get('hldg_qty', '0')                # 보유수량
                current_value = int(item.get("evlu_amt", 0))   # 평단
                profit_amount = int(item.get("evlu_pfls_amt", 0)) # 수익금
                profit_rt = float(item.get('evlu_pfls_rt', 0)) # 수익률

                stock.append({
                    "code":code,
                    "name" : name,
                    "qty" : qty,
                    "current_value" : current_value,
                    "profit_amount" : profit_amount,
                    "profit_rt": profit_rt
                })

        return stock