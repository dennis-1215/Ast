from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QLineEdit, QFrame, QPushButton,
                               QGraphicsDropShadowEffect, QScrollArea)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

import webbrowser # 뉴스 url을 위해 임포트

from Api import api_handler

# Utils
from UI.Utils.timers import TimerManager
from UI.Utils.time_utils import *
from UI.Utils.image_utils import ImageUtils

# Style
from UI.Styles.theme import *

# Components
from UI.Components.search_bar import SearchBar
from UI.Components.base_card import BaseCard
from UI.Components.news_ticker import NewsTicker
from UI.Components.stock_ranking_panel import StockRankingPanel

class StockItemWidget(QFrame):
    """리스트에 들어갈 개별 종목 위젯 (클릭 가능)"""
    clicked = Signal(str)  # 종목 코드를 전달할 시그널

    def __init__(self, rank, name, price, change_rate, code):
        super().__init__()
        self.code = code
        self.setObjectName("StockItem")
        self.setFixedHeight(70)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)

        # 왼쪽: 순위와 이름
        name_info_layout = QHBoxLayout()
        rank_label = QLabel(str(rank))
        rank_label.setFixedWidth(20)
        rank_label.setStyleSheet(f"color:{TEXT_SUB}; font-weight: bold; font-size: {FONT_SM};")

        name_label = QLabel(name)
        name_label.setStyleSheet(f"font-size:{FONT_MD}; font-weight: 600; color: {TEXT_NAME};")

        name_info_layout.addWidget(rank_label)
        name_info_layout.addWidget(name_label)
        name_info_layout.addStretch()

        # 오른쪽: 가격 및 등락률
        price_layout = QVBoxLayout()
        price_label = QLabel(f"{price}원")
        price_label.setStyleSheet(f"font-size: 15px; font-weight: 500; color: {TEXT_NAME};")

        # 등락률 색상 처리
        is_up = "+" in change_rate or (change_rate.replace('%', '').strip() != '0' and "-" not in change_rate)
        color = RED if is_up else BLUE
        change_label = QLabel(change_rate)
        change_label.setStyleSheet(f"color: {color}; font-weight: 500; font-size: 13px;")

        price_layout.addWidget(price_label, alignment=Qt.AlignmentFlag.AlignRight)
        price_layout.addWidget(change_label, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(name_info_layout)
        layout.addLayout(price_layout)

        self.setStyleSheet(f"""
            #StockItem {{
                background-color: white;
                border-radius: {FONT_XS};
                margin-bottom: 2px;
            }}
            #StockItem:hover {{
                background-color: {HOVER};
            }}
        """)

    def mousePressEvent(self, event):
        self.clicked.emit(self.code)

class TradingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Trading Program")
        self.resize(1280, 800)
        self.setStyleSheet(f"background-color: {BACKGROUND};")  # 전체 배경색

        self.api = api_handler.KisApi()
        self.timer_manager = TimerManager(self)

        # 메인 컨테이너 (Vertical)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)



        # 뉴스 호출 및 저장
        api_news = api_handler.get_naver_news("주식 시장", 10)
        if api_news:
            self.news_data = api_news
        else:
            # API 실패 시 보여줄 기본 데이터 (백업용)
            self.news_data = [{"title": "📢 실시간 뉴스를 불러올 수 없습니다.", "url": ""}]

        self.news_index = 0

        # 메인화면 레이아웃
        self.create_top_area()
        self.create_main_body()
        self.create_bottom_dock()

        # 자산 현황 업데이트
        self.update_asset_data()

        # 시간 표시용 타이머 객체 생성
        self.timer_manager.create_timer(
            name= "clock",
            interval= 1000,
            callback= self.update_clock_ui
        )
        # 시간을 받아오는 TimeUtils 생성
        self.clock = TimeUtils()
        # 초기 시간 즉시 표시
        self.update_clock_ui()


    def update_clock_ui(self):
        self.time_label.setText(self.clock.get_live_clock_text())

    # 뉴스 로테이션 함수
    def rotate_news(self):
        self.news_index = (self.news_index + 1) % len(self.news_data)
        new_title = self.news_data[self.news_index]["title"]
        self.news_btn.setText(new_title)

    # 브라우저 열기 함수
    def open_news_url(self):
        url = self.news_data[self.news_index]["url"]
        webbrowser.open(url)  # 시스템 기본 브라우저로 URL 실행

    # 자산 업데이트 함수
    def update_asset_data(self):

        # 1. 자산 현황 (총 평가금액, 손익금액) 가져오기
        asset_status = self.api.get_asset_status()
        if asset_status:
            # API 명세서 기준 데이터 파싱
            total_asset = int(asset_status[0].get('tot_evlu_amt', 0))  # 총 평가 금액
            profit_loss = int(asset_status[0].get('evlu_pfls_smtl_amt', 0))  # 평가 손익 금액

            # 수익률 계산 (총 평가 금액 - 평가 손익 = 투자 원금)
            principal = total_asset - profit_loss
            profit_rate = (profit_loss / principal * 100) if principal > 0 else 0

            # 자산 텍스트 업데이트 (천 단위 콤마)
            self.asset_val_label.setText(f"₩{total_asset:,}")

            # 수익 여부에 따른 뱃지 색상 및 기호 변경
            if profit_loss > 0:
                badge_style = f"background-color: #FEEEEE; color: {RED}; font-weight: bold; padding: 5px 10px; border-radius: 8px;"
                badge_text = f"+{profit_rate:.2f}% (↑ ₩{profit_loss:,})"
            elif profit_loss < 0:
                badge_style = f"background-color: #E8F3FF; color: {PRIMARY}; font-weight: bold; padding: 5px 10px; border-radius: 8px;"
                badge_text = f"{profit_rate:.2f}% (↓ ₩{abs(profit_loss):,})"
            else:
                badge_style = "background-color: #F2F4F6; color: #4E5968; font-weight: bold; padding: 5px 10px; border-radius: 8px;"
                badge_text = f"0.00% (- ₩0)"

            self.profit_badge.setStyleSheet(badge_style)
            self.profit_badge.setText(badge_text)

        # 2. 보유 종목 리스트 가져오기
        balance = self.api.get_balance()
        if balance:
            # 기존에 그려진 종목 리스트가 있다면 초기화 (addStretch 남기고 삭제)
            for i in reversed(range(self.stock_list_layout.count() - 1)):
                widget = self.stock_list_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

            # 종목별 라벨 생성 및 추가
            for item in balance:
                name = item.get('prdt_name', '알수없음')  # 종목명 [cite: 216]
                qty = item.get('hldg_qty', '0')  # 보유수량 [cite: 216]
                profit_rt = float(item.get('evlu_pfls_rt', 0))  # 수익률 [cite: 216]

                # 색상 결정
                color = "#F04452" if profit_rt > 0 else "#3182F6" if profit_rt < 0 else "#4E5968"

                # 종목명(보유수량) 수익률 텍스트 라벨
                stock_text = f"<span style='color:{TEXT_MAIN};'>{name}</span> " \
                             f"<span style='color:{TEXT_SUB}; font-size:{FONT_XS};'>({qty}주)</span> " \
                             f"<span style='color:{color}; font-weight:bold;'>{profit_rt:.2f}%</span>"

                stock_label = QLabel(stock_text)
                stock_label.setStyleSheet(f"font-size: {FONT_SM}; margin-bottom: 5px;")

                # 리스트 레이아웃의 상단(addStretch 이전)에 삽입
                self.stock_list_layout.insertWidget(self.stock_list_layout.count() - 1, stock_label)
        else:
            empty_label = QLabel("보유한 종목이 없습니다")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("""
                    font-family: 'Pretendard';
                    color: #444444;
                    font-size: 18px;
                    font-weight: 600;
                """)
            empty_label.setMinimumHeight(320)

            # addStretch 이전 위치에 삽입
            self.stock_list_layout.insertWidget(
                self.stock_list_layout.count() - 1,
                empty_label
            )

    def create_top_area(self):
        top_widget = QWidget()
        top_widget.setFixedHeight(70)
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(25, 15, 25, 0)
        top_layout.setSpacing(5)

        # --- 1. 왼쪽 컨테이너 (로고 및 시간) ---
        left_container = QWidget()
        left_layout = QHBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 내용물 왼쪽 정렬

        # 아이콘 라벨 생성
        logo_icon = QLabel()
        logo_icon.setPixmap(ImageUtils.load_pixmap("Logo.png", 60, 60))
        left_layout.addWidget(logo_icon)

        self.time_label = QLabel()
        self.time_label.setStyleSheet(f"color: #4E5968; font-size: {FONT_XS};")

        self.logo_title = QLabel("STOCK TRADING PROGRAM")
        self.logo_title.setStyleSheet(f"font-weight: bold; color: #333D4B; font-size: {FONT_SM};")

        text_vbox = QVBoxLayout()
        text_vbox.setContentsMargins(0, 13, 0, 13)
        text_vbox.addWidget(self.logo_title)
        text_vbox.addWidget(self.time_label)
        left_layout.addLayout(text_vbox)


        # --- 2. 중앙 컨테이너 (검색창) ---
        mid_container = QWidget()
        mid_layout = QHBoxLayout(mid_container)
        mid_layout.setContentsMargins(0, 0, 0, 0)
        mid_layout.setAlignment(Qt.AlignCenter)  # 내용물 중앙 정렬


        # 검색창 컨테이너 (QFrame)
        self.search_bar = SearchBar(placeholder="삼성전자, 005930, 테마 검색")
        self.search_bar.search_requested.connect(self.on_search)
        mid_layout.addWidget(self.search_bar)

        # --- 3. 오른쪽 컨테이너 (뉴스 헤드라인) ---
        right_container = QWidget()
        right_layout = QHBoxLayout(right_container)
        right_layout.setContentsMargins(50, 0, 0, 0)
        right_layout.setAlignment(Qt.AlignLeft)

        self.news_ticker = NewsTicker()
        self.news_ticker.set_news(self.news_data)
        right_layout.addWidget(self.news_ticker)

        # 뉴스 순환용 타이머 설정
        self.timer_manager.create_timer(
            name="news_rotate",
            interval=5000,
            callback=self.news_ticker.next_news
        )

        # --- 4. 메인 레이아웃에 1:1:1 비율로 추가 ---
        top_layout.addWidget(left_container, 1)  # 비율 1
        top_layout.addWidget(mid_container, 1)  # 비율 1
        top_layout.addWidget(right_container, 1)  # 비율 1

        self.main_layout.addWidget(top_widget)

    def create_main_body(self):
        body_widget = QWidget()
        body_layout = QHBoxLayout(body_widget)
        body_layout.setContentsMargins(25, 10, 25, 20)
        body_layout.setSpacing(20)

        # 카드 생성 (좌, 중, 우)
        self.card_left = BaseCard("My Assets (내 자산)")
        self.card_mid = BaseCard("Market Rankings (실시간 순위)")
        self.card_right = BaseCard("Quick View (즐겨찾기)")

        # 레이아웃 추가 및 비율(Stretch) 설정 (1:1:1)
        body_layout.addWidget(self.card_left, 1)
        body_layout.addWidget(self.card_mid, 1)
        body_layout.addWidget(self.card_right, 1)

        # 좌측 카드 내부 채우기
        self.setup_left_card()

        # 중앙 카드 내부 채우기
        self.setup_center_card()

        self.main_layout.addWidget(body_widget)

    def create_card(self, title):
        card = QFrame()
        card.setObjectName("Card")
        card.setStyleSheet(f"""
            #Card {{
                background-color: white;
                border-radius: 24px;
                border: 1px solid {BORDER};
            }}
        """)

        # 그림자 효과
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 20))
        shadow.setOffset(0, 4)
        card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333D4B; background-color: white")
        layout.addWidget(title_label)
        layout.addSpacing(15)

        return card

    def setup_left_card(self):
        layout = self.card_left.layout()

        # 총 자산 섹션
        self.asset_val_label = QLabel("자산 불러오는 중...")
        self.asset_val_label.setStyleSheet(f"font-size: {FONT_XL}; font-weight: 800; color: {TEXT_MAIN}; background-color: white")
        layout.addWidget(self.asset_val_label)

        # 수익률 뱃지
        profit_layout = QHBoxLayout()
        self.profit_badge = QLabel("-")
        self.profit_badge.setStyleSheet(f"""
            background-color: #FEEEEE; 
            color: {RED}; 
            font-weight: bold; 
            padding: 5px 10px; 
            border-radius: 8px;
        """)
        profit_layout.addWidget(self.profit_badge)
        profit_layout.addStretch()
        layout.addLayout(profit_layout)

        layout.addSpacing(20)
        layout.addWidget(QLabel("보유 종목 리스트"))

        # 보유 종목 리스트를 담을 스크롤 영역 또는 프레임 내부 레이아웃
        list_frame = QFrame()
        list_frame.setStyleSheet(f"background-color: {HOVER}; border-radius: {RADIUS_ITEM};")

        # 보유 종목들이 세로로 쌓일 레이아웃 생성
        self.stock_list_layout = QVBoxLayout(list_frame)
        self.stock_list_layout.setContentsMargins(15, 15, 15, 15)
        self.stock_list_layout.addStretch()  # 데이터가 위에서부터 쌓이도록 아래 여백 추가

        layout.addWidget(list_frame, 1)  # 남은 공간 채우기

    def setup_center_card(self):
        layout = self.card_mid.layout()

        self.ranking_panel = StockRankingPanel()
        layout.addWidget(self.ranking_panel)

        # 테스트 데이터 연결 예시
        test_data = [
            {"name": "삼성전자", "price": 72500, "change_rate": "+1.2%", "code": "005930"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
            {"name": "SK하이닉스", "price": 185000, "change_rate": "-0.5%", "code": "000660"},
        ]
        self.ranking_panel.update_list(test_data)

    def on_search(self, keyword):
        print(f"검색 요청 : {keyword}")
        # TODO: 종목 검색 API 연결 예정

    def get_tab_style(self, active=False):
        if active:
            return f"""
                QPushButton {{
                    background-color: {PRIMARY};
                    color: white;
                    border-radius: 18px;
                    font-weight: bold;
                    border: none;
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background-color: {BORDER};
                    color: #4E5968;
                    border-radius: 18px;
                    font-weight: medium;
                    border: none;
                }}
                QPushButton:hover {{
                    background-color: {SCROLLBAR};
                }}
            """

    def on_tab_clicked(self, tab_key):
        # 다른 버튼들 스타일 초기화 및 선택된 버튼 강조
        for key, btn in self.tab_buttons.items():
            if key == tab_key:
                btn.setChecked(True)
                btn.setStyleSheet(self.get_tab_style(active=True))
            else:
                btn.setChecked(False)
                btn.setStyleSheet(self.get_tab_style(active=False))

        print(f"Tab {tab_key} clicked! 여기서 API 데이터를 불러오면 됩니다.")


    def create_bottom_dock(self):
        dock_container = QWidget()
        dock_container.setFixedHeight(100)
        dock_layout = QHBoxLayout(dock_container)

        # 독 바 (실제 메뉴)
        dock_bar = QFrame()
        dock_bar.setFixedSize(500, 70)
        dock_bar.setStyleSheet(f"""
            background-color: white; 
            border-radius: 35px; 
            border: 1px solid {BORDER};
        """)

        # 버튼들 배치
        menu_layout = QHBoxLayout(dock_bar)
        menu_layout.setContentsMargins(20, 0, 20, 0)

        menus = [("🏠", "홈"), ("⭐", "즐겨찾기"), ("💡", "매매전략"), ("📊", "전략분석")]
        for icon, name in menus:
            btn = QPushButton(f"{icon}\n{name}")
            btn.setStyleSheet("border: none; color: #4E5968; font-size: 11px; font-weight: bold;")
            menu_layout.addWidget(btn)

        dock_layout.addWidget(dock_bar, 0, Qt.AlignCenter)
        self.main_layout.addWidget(dock_container)



