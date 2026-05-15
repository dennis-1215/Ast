from PySide6.QtWidgets import (QWidget, QVBoxLayout,
                               QHBoxLayout)

from Api import api_handler

# Services
from Core.services.asset_service import AssetService
from Core.services.news_service import NewsService

# Utils
from UI.Utils.timers import TimerManager
from UI.Utils.time_utils import *

# Style

# Components
from UI.Components.base_card import BaseCard
from UI.Components.stock_ranking_panel import StockRankingPanel
from UI.Components.top_bar import TopBar
from UI.Components.dock_bar import DockBar

# Sections
from UI.Sections.asset.asset_section import AssetSection

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        # API 핸들러 생성
        self.api = api_handler.KisApi()

        # 타이머 매니저 생성
        self.timer_manager = TimerManager(self)

        # 서비스 객체 생성
        self.asset_service = AssetService(self.api)
        self.news_service = NewsService(self.api)

        # 메인 컨테이너 (Vertical)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 메인화면 레이아웃
        self.top_bar = TopBar(self.news_service.get_news_data())
        self.main_layout.addWidget(self.top_bar)
        self.top_bar.search_bar.search_requested.connect(self.on_search)
        self.timer_manager.create_timer(
            name="news_timer",
            interval=5000,
            callback=self.top_bar.news_ticker.next_news
        )


        self.create_main_body()

        self.asset_section.controller.balance_loaded.connect(self.on_balance_loaded)

        self.dock_bar = DockBar()
        self.dock_bar.menu_clicked.connect(self.on_menu_changed)
        self.main_layout.addWidget(self.dock_bar)

        # 자산 현황 업데이트
        self.refresh_asset_data()

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
        self.top_bar.update_clock(self.clock.get_live_clock_text())

    # 자산 업데이트 함수
    def refresh_asset_data(self):
        self.asset_section.refresh()

    def create_main_body(self):
        body_widget = QWidget()
        body_layout = QHBoxLayout(body_widget)
        body_layout.setContentsMargins(25, 10, 25, 20)
        body_layout.setSpacing(20)

        # 카드 생성 (좌, 중, 우)
        self.asset_section = AssetSection(self.asset_service)

        self.card_mid = BaseCard("Market Rankings (실시간 순위)")
        self.card_right = BaseCard("Quick View (즐겨찾기)")

        # 레이아웃 추가 및 비율(Stretch) 설정 (1:1:1)
        body_layout.addWidget(self.asset_section, 1)
        body_layout.addWidget(self.card_mid, 1)
        body_layout.addWidget(self.card_right, 1)

        # 중앙 카드 내부 채우기
        self.setup_center_card()

        self.main_layout.addWidget(body_widget)

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

    # dock_bar에서 사용될 함수
    def on_menu_changed(self, menu):
        print(f"{menu} 메뉴 클릭")

    # 자산 및 보유주식 호출 상태 처리
    def on_balance_loaded(self, success):
        if success:
            print("자산 로딩 성공")
        else:
            print("자산 로딩 실패")

            # 2초 뒤 재시도
            self.timer_manager.create_timer(
                name="retry_asset_load",
                interval=2000,
                callback=self.refresh_asset_data,
                single_shot=True
            )