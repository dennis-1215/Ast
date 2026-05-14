import sys
import os

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QLineEdit, QFrame, QPushButton,
                               QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy,
                               QScrollArea)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QColor, QFont
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer, QDateTime

import webbrowser # 뉴스 url을 위해 임포트
import api_handler


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
        rank_label.setStyleSheet("color: #8B95A1; font-weight: bold; font-size: 14px;")

        name_label = QLabel(name)
        name_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #333D4B;")

        name_info_layout.addWidget(rank_label)
        name_info_layout.addWidget(name_label)
        name_info_layout.addStretch()

        # 오른쪽: 가격 및 등락률
        price_layout = QVBoxLayout()
        price_label = QLabel(f"{price}원")
        price_label.setStyleSheet("font-size: 15px; font-weight: 500; color: #333D4B;")

        # 등락률 색상 처리
        is_up = "+" in change_rate or (change_rate.replace('%', '').strip() != '0' and "-" not in change_rate)
        color = "#F04452" if is_up else "#3182F6"
        change_label = QLabel(change_rate)
        change_label.setStyleSheet(f"color: {color}; font-weight: 500; font-size: 13px;")

        price_layout.addWidget(price_label, alignment=Qt.AlignmentFlag.AlignRight)
        price_layout.addWidget(change_label, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(name_info_layout)
        layout.addLayout(price_layout)

        self.setStyleSheet("""
            #StockItem {
                background-color: white;
                border-radius: 12px;
                margin-bottom: 2px;
            }
            #StockItem:hover {
                background-color: #F9FAFB;
            }
        """)

    def mousePressEvent(self, event):
        self.clicked.emit(self.code)


class StockRankingPanel(QWidget):
    """중앙 메인 랭킹 패널"""

    def __init__(self, api_instance):
        super().__init__()
        self.api = api_instance
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 0)
        layout.setSpacing(15)

        # 1. 상단 탭 버튼 영역
        self.tab_container = QFrame()
        self.tab_layout = QHBoxLayout(self.tab_container)
        self.tab_layout.setContentsMargins(0, 0, 0, 0)
        self.tab_layout.setSpacing(8)

        self.tabs = {
            "거래량": QPushButton("거래량"),
            "상승률": QPushButton("상승률"),
            "배당률": QPushButton("배당률")
        }

        tab_style = """
            QPushButton {
                padding: 8px 16px;
                border: none;
                border-radius: 18px;
                background-color: #E5E8EB;
                color: #4E5968;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:checked {
                background-color: #3182F6;
                color: white;
            }
        """

        for name, btn in self.tabs.items():
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.setStyleSheet(tab_style)
            btn.clicked.connect(lambda checked, n=name: self.update_list(n))
            self.tab_layout.addWidget(btn)

        self.tab_layout.addStretch()
        self.tabs["거래량"].setChecked(True)
        layout.addWidget(self.tab_container)

        # 2. 스크롤 가능한 리스트 영역
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("background-color: transparent;")

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: transparent;")
        self.list_layout = QVBoxLayout(self.scroll_content)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(10)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        # 초기 리스트 로드
        self.update_list("거래량")

    def update_list(self, category):
        # 기존 아이템 삭제
        for i in reversed(range(self.list_layout.count())):
            widget = self.list_layout.itemAt(i).widget()
            if widget: widget.setParent(None)

        # TODO: self.api (KisApi)를 이용해 실제 데이터를 가져오는 로직 연결
        # 현재는 구조 확인을 위한 샘플 데이터입니다.
        sample_data = self.get_mock_data(category)

        for data in sample_data:
            item = StockItemWidget(data['rank'], data['name'], data['price'], data['change'], data['code'])
            item.clicked.connect(self.handle_stock_click)
            self.list_layout.addWidget(item)

    def get_mock_data(self, category):
        # API 연동 전 테스트용 데이터
        return [
            {"rank": i + 1, "name": f"{category} 종목 {i + 1}", "price": "75,000", "change": "+2.5%", "code": "005930"}
            for i in range(20)  # API가 주는 만큼 스크롤 가능하게 생성
        ]

    def handle_stock_click(self, code):
        print(f"종목 클릭됨: {code} (상세 페이지 로직 연결 예정)")

class TradingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Trading Program")
        self.resize(1280, 800)
        self.setStyleSheet("background-color: #F2F4F6;")  # 전체 배경색

        self.api = api_handler.KisApi()

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

        # 뉴스 순환용 타이머 설정
        self.news_timer = QTimer(self)
        self.news_timer.timeout.connect(self.rotate_news)
        self.news_timer.start(5000)  # 5초마다 교체

        # 메인화면 레이아웃
        self.create_top_area()
        self.create_main_body()
        self.create_bottom_dock()

        # 자산 현황 업데이트
        self.update_asset_data()

        # 시간 표시용 타이머 객체 생성
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        # 초기 시간 즉시 표시
        self.update_clock()


    def update_clock(self):
        current_time = QDateTime.currentDateTime().toString("hh:mm:ss A")
        self.time_label.setText(f"Live | {current_time}")

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
                badge_style = "background-color: #FEEEEE; color: #F04452; font-weight: bold; padding: 5px 10px; border-radius: 8px;"
                badge_text = f"+{profit_rate:.2f}% (↑ ₩{profit_loss:,})"
            elif profit_loss < 0:
                badge_style = "background-color: #E8F3FF; color: #3182F6; font-weight: bold; padding: 5px 10px; border-radius: 8px;"
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
                stock_text = f"<span style='color:#191F28;'>{name}</span> " \
                             f"<span style='color:#8B95A1; font-size:12px;'>({qty}주)</span> " \
                             f"<span style='color:{color}; font-weight:bold;'>{profit_rt:.2f}%</span>"

                stock_label = QLabel(stock_text)
                stock_label.setStyleSheet("font-size: 14px; margin-bottom: 5px;")

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
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "Images", "Logo.png")
        pixmap = QPixmap(image_path)  # 이미지 파일 경로
        logo_icon.setPixmap(pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        left_layout.addWidget(logo_icon)

        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: #4E5968; font-size: 12px;")

        self.logo_title = QLabel("STOCK TRADING PROGRAM")
        self.logo_title.setStyleSheet("font-weight: bold; color: #333D4B; font-size: 14px;")

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
        search_container = QFrame()
        search_container.setFixedSize(470, 40)
        search_container.setStyleSheet("""
            background-color: white; 
            border-radius: 20px; 
            border: 1px solid #E5E8EB;
        """)
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(15, 0, 15, 0)

        search_icon = QLabel()  # 나중에 이미지(Pixmap)로 교체 가능
        image_path = os.path.join(current_dir, "Images", "search.png")
        pixmap = QPixmap(image_path)  # 이미지 파일 경로
        # 아이콘 크기를 적절하게 조절 (예: 20x20)
        search_icon.setPixmap(pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        search_icon.setStyleSheet("border: none; background-color: transparent;")

        search_input = QLineEdit()
        search_input.setPlaceholderText("삼성전자, 005930, 테마 검색")
        search_input.setStyleSheet("border: none; background: transparent; font-size: 14px;")

        search_layout.addWidget(search_icon)
        search_layout.addWidget(search_input)

        mid_layout.addWidget(search_container)

        # --- 3. 오른쪽 컨테이너 (뉴스 헤드라인) ---
        right_container = QWidget()
        right_layout = QHBoxLayout(right_container)
        right_layout.setContentsMargins(50, 0, 0, 0)
        right_layout.setAlignment(Qt.AlignLeft)

        self.news_btn = QLabel(self.news_data[0]["title"], self)
        self.news_btn.setFixedWidth(320)
        self.news_btn.setWordWrap(True)
        self.news_btn.setCursor(Qt.PointingHandCursor)
        self.news_btn.mousePressEvent = lambda event: self.open_news_url()

        self.news_btn.setStyleSheet("""
            QLabel {
                color: #4E5968;
                font-size: 13px;
                border: none;
                background: transparent;
                qproperty-alignment: 'AlignLeft | AlignVCenter';
            }
            QLabel:hover {
                text-decoration: underline;
                color: #3182F6; 
            }
        """)

        right_layout.addWidget(self.news_btn)


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
        self.card_left = self.create_card("My Assets (내 자산)")
        self.card_mid = self.create_card("Market Rankings (실시간 순위)")
        self.card_right = self.create_card("Quick View (즐겨찾기)")

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
        card.setStyleSheet("""
            #Card {
                background-color: white;
                border-radius: 24px;
                border: 1px solid #E5E8EB;
            }
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
        self.asset_val_label.setStyleSheet("font-size: 28px; font-weight: 800; color: #191F28; background-color: white")
        layout.addWidget(self.asset_val_label)

        # 수익률 뱃지
        profit_layout = QHBoxLayout()
        self.profit_badge = QLabel("-")
        self.profit_badge.setStyleSheet("""
            background-color: #FEEEEE; 
            color: #F04452; 
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
        list_frame.setStyleSheet("background-color: #F9FAFB; border-radius: 12px;")

        # 보유 종목들이 세로로 쌓일 레이아웃 생성
        self.stock_list_layout = QVBoxLayout(list_frame)
        self.stock_list_layout.setContentsMargins(15, 15, 15, 15)
        self.stock_list_layout.addStretch()  # 데이터가 위에서부터 쌓이도록 아래 여백 추가

        layout.addWidget(list_frame, 1)  # 남은 공간 채우기

    def setup_center_card(self):
        layout = self.card_mid.layout()
        layout.setSpacing(15)

        # 1. 상단 타이틀 및 탭 영역
        header_layout = QVBoxLayout()

        title = QLabel("오늘의 종목 랭킹")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #191F28; margin-bottom: 5px;")
        header_layout.addWidget(title)

        # 탭 버튼들을 담을 레이아웃 (거래량, 상승률, 배당률)
        tab_layout = QHBoxLayout()
        self.tab_buttons = {}
        tabs = [("volume", "거래량"), ("rising", "상승률"), ("dividend", "배당률")]

        for key, name in tabs:
            btn = QPushButton(name)
            btn.setCheckable(True)  # 클릭된 상태 유지 가능하게
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedSize(80, 36)
            btn.setStyleSheet(self.get_tab_style())

            # 기본값으로 '거래량' 활성화
            if key == "volume":
                btn.setChecked(True)
                btn.setStyleSheet(self.get_tab_style(active=True))

            # 클릭 이벤트 연결 (나중에 구현할 API 호출 함수 등)
            btn.clicked.connect(lambda checked, k=key: self.on_tab_clicked(k))

            tab_layout.addWidget(btn)
            self.tab_buttons[key] = btn

        tab_layout.addStretch()
        header_layout.addLayout(tab_layout)
        layout.addLayout(header_layout)

        # 2. 종목 리스트 스크롤 영역
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none; background-color: transparent;")

        # 스크롤 내부에 들어갈 실제 위젯
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: transparent;")
        self.ranking_list_layout = QVBoxLayout(self.scroll_content)
        self.ranking_list_layout.setContentsMargins(0, 5, 0, 0)
        self.ranking_list_layout.setSpacing(10)
        self.ranking_list_layout.addStretch()  # 아래쪽 여백

        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

    def get_tab_style(self, active=False):
        if active:
            return """
                QPushButton {
                    background-color: #3182F6;
                    color: white;
                    border-radius: 18px;
                    font-weight: bold;
                    border: none;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: #E5E8EB;
                    color: #4E5968;
                    border-radius: 18px;
                    font-weight: medium;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #D1D6DB;
                }
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
        dock_bar.setStyleSheet("""
            background-color: white; 
            border-radius: 35px; 
            border: 1px solid #E5E8EB;
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



app = QApplication(sys.argv)

# 폰트 설정 (시스템에 Pretendard가 있다면 적용)
font = QFont("Pretendard", 10)
app.setFont(font)

window = TradingApp()
window.show()
sys.exit(app.exec())