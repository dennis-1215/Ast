import requests
import json
import sqlite3
import pandas as pd
import time
import FinanceDataReader as fdr
from datetime import datetime
import AppKeys

# ---------------------------------------------------------------------------------------
# 한국 투자증권 API
# ---------------------------------------------------------------------------------------
class KisApi:
    def __init__(self, is_paper_trading = True):
        # 1. 설정 정보 초기화
        self.app_key = AppKeys.APP_KEY
        self.app_secret = AppKeys.APP_SECRET
        self.acc_no = AppKeys.paper_account if is_paper_trading else AppKeys.real_account
        self.acc_no_prefix = "01"
        self.is_paper = is_paper_trading

        # URL 설정
        if self.is_paper:
            self.base_url = "https://openapivts.koreainvestment.com:29443"
        else:
            self.base_url = "https://openapi.koreainvestment.com:9443"

        # 토큰 자동 발급
        self.token = self.get_access_token()
        self.db_path = 'trading_system.db'

    # --- [인증 및 토큰] ---
    def get_access_token(self):
        url = f"{self.base_url}/oauth2/tokenP"
        headers = {"content-type": "application/json"}
        body = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }
        res = requests.post(url, headers=headers, data=json.dumps(body))
        if res.status_code == 200:
            token = res.json().get('access_token')
            print(f"✅ 토큰 발행 성공: {token[:10]}...")
            return token
        print("❌ 토큰 발행 실패")
        return None

    # --- [자산 연동 기능] ---
    def get_balance(self):
        """현재 계좌의 주식 잔고 및 수익률 조회"""
        path = "/uapi/domestic-stock/v1/trading/inquire-balance"
        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {self.token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": "VTTC8434R" if self.is_paper else "TTTC8434R"
        }
        params = {
            "CANO": self.acc_no,
            "ACNT_PRDT_CD": self.acc_no_prefix,
            "AFHR_FLPR_YN": "N",
            "OFL_YN": "",
            "INQR_DVSN": "02",
            "UNPR_DVSN": "01",
            "FUND_STTL_ICLD_YN": "N",
            "FNCG_AMT_AUTO_RDPT_YN": "N",
            "PRCS_DVSN": "00",
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": ""
        }
        res = requests.get(f"{self.base_url}{path}", headers=headers, params=params)
        return res.json().get('output1', [])

    def get_asset_status(self):
        """총 평가액, 예수금 등 계좌 자산 현황 조회"""
        path = "/uapi/domestic-stock/v1/trading/inquire-account-balance"
        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {self.token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": "VTTC8434R" if self.is_paper else "TTTC8434R"
        }
        params = {
            "CANO": self.acc_no,
            "ACNT_PRDT_CD": self.acc_no_prefix,
            "AFHR_FLPR_YN": "N",
            "OFL_YN": "",
            "INQR_DVSN": "02",
            "UNPR_DVSN": "01",
            "FUND_STTL_ICLD_YN": "N",
            "FNCG_AMT_AUTO_RDPT_YN": "N",
            "PRCS_DVSN": "00",
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": ""
        }
        res = requests.get(f"{self.base_url}{path}", headers=headers, params=params)

        if res:
            print("자산 불러오기 성공")
        else:
            print("자산 불러오기 실패")

        return res.json().get('output2', [])

    # --- [순위 호출 기능] ---
    def get_ranking_stocks(self, tab_key):
        self.base_url = "https://openapi.koreainvestment.com:9443"


    # --- [시장 데이터 수집 및 DB] ---
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS daily_prices (
                ticker TEXT, date TEXT, open INTEGER, high INTEGER, low INTEGER, 
                close INTEGER, volume INTEGER, change_val INTEGER, 
                change_rate REAL, sign TEXT, PRIMARY KEY (ticker, date)
            )
        ''')
        cur.execute('CREATE TABLE IF NOT EXISTS stock_info (ticker TEXT PRIMARY KEY, name TEXT)')
        conn.commit()
        return conn

    def fetch_and_save_past_data(self, ticker, conn):
        path = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {self.token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": "FHKST03010100",
            "custtype": "P"
        }
        params = {
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": ticker,
            "fid_input_date_1": "20240101",
            "fid_input_date_2": datetime.now().strftime("%Y%m%d"),
            "fid_period_div_code": "D",
            "fid_org_adj_prc": "1"
        }
        res = requests.get(f"{self.base_url}{path}", headers=headers, params=params)

        if res.status_code == 200:
            data = res.json()
            output2 = data.get('output2', [])
            if not output2: return

            df = pd.DataFrame(output2)
            df = df[['stck_bsop_date', 'stck_oprc', 'stck_hgpr', 'stck_lwpr', 'stck_clpr',
                     'acml_vol', 'prdy_vrss', 'prdy_vrss_sign']]
            df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'change_val', 'sign']

            for col in ['open', 'high', 'low', 'close', 'volume', 'change_val']:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

            df = df.sort_values(by='date', ascending=True)
            df['change_rate'] = (df['close'].pct_change() * 100).round(2).fillna(0.0)
            df['ticker'] = ticker

            try:
                df = df[
                    ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume', 'change_val', 'change_rate', 'sign']]
                df.to_sql('daily_prices', conn, if_exists='append', index=False)
            except sqlite3.IntegrityError:
                pass
        else:
            print(f"❌ {ticker} 호출 실패: {res.text}")

    def collect_full_market_data(self):
        """전체 종목 리스트 업데이트 및 데이터 수집 실행"""
        conn = self.init_db()

        # 1. 종목 정보 업데이트
        print("🔍 한국거래소(KRX)에서 종목 리스트를 불러오는 중...")
        df_kospi = fdr.StockListing('KOSPI')[['Code', 'Name']]
        df_kosdaq = fdr.StockListing('KOSDAQ')[['Code', 'Name']]
        df_info = pd.concat([df_kospi, df_kosdaq])
        df_info.columns = ['ticker', 'name']
        df_info.to_sql('stock_info', conn, if_exists='replace', index=False)

        # 2. 수집 대상 선정
        existing_tickers = pd.read_sql("SELECT DISTINCT ticker FROM daily_prices", conn)['ticker'].tolist()
        target_tickers = [t for t in df_info['ticker'].tolist() if t not in existing_tickers]

        total = len(target_tickers)
        name_dict = df_info.set_index('ticker')['name'].to_dict()
        start_time = time.time()

        for i, ticker in enumerate(target_tickers):
            try:
                print(f"[{i + 1}/{total}] {name_dict.get(ticker, ticker)} 데이터 수집 중...")
                self.fetch_and_save_past_data(ticker, conn)
                time.sleep(0.6)  # API 제한 준수

                if (i + 1) % 20 == 0:
                    elapsed = (time.time() - start_time) / 60
                    print(f"📊 진행률: {((i + 1) / total) * 100:.1f}% | 소요시간: {elapsed:.1f}분")
            except Exception as e:
                print(f"⚠️ {ticker} 에러: {e}")
                continue

        conn.close()
        print("🏁 전체 데이터 구축 완료.")

# ---------------------------------------------------------------------------------------
# 네이버 API
# ---------------------------------------------------------------------------------------

def get_naver_news(query="주식", display=10):
    """
    네이버 뉴스 API를 통해 뉴스 제목과 URL을 가져옵니다.
    """
    client_id = AppKeys.Naver_ID
    client_secret = AppKeys.Naver_Secret

    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display={display}&sort=sim"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }

    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            items = res.json().get('items', [])
            formatted_news = []
            for item in items:
                # <b> 태그 제거 및 데이터 정제
                title = item['title'].replace("<b>", "").replace("</b>", "").replace("&quot;", "\"")
                formatted_news.append({
                    "title": f"📢 {title}",
                    "url": item['link']  # 기사 URL 제공됨
                })
            return formatted_news
    except Exception as e:
        print(f"네이버 뉴스 로드 중 오류: {e}")
    return []

if __name__ == "__main__":
    pass