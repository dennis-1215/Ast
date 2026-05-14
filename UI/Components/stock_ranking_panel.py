from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QFrame
from PySide6.QtCore import Qt
from UI.Styles.theme import *
from UI.Components.stock_item import StockItemWidget


class StockRankingPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(15)

        # 1. 상단 탭 레이아웃
        self.tab_layout = QHBoxLayout()
        self.tab_layout.setSpacing(10)  # 버튼 사이 간격
        self.tab_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # 왼쪽 정렬 고정

        self.tab_buttons = {}
        tabs = [("volume", "거래량"), ("rise", "상승률"), ("dividend", "배당률")]

        for key, text in tabs:
            btn = QPushButton(text)
            btn.setCheckable(True)
            # 고정 크기 설정 (텍스트가 변해도 크기가 바뀌지 않도록)
            btn.setFixedSize(70, 35)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

            btn.clicked.connect(lambda checked, k=key: self.on_tab_clicked(k))
            self.tab_buttons[key] = btn
            self.tab_layout.addWidget(btn)

        # 중요: 버튼들을 왼쪽으로 밀어주고 남은 공간을 차지함
        self.tab_layout.addStretch()
        self.main_layout.addLayout(self.tab_layout)

        # 초기 스타일 적용 (거래량 탭 활성화)
        self.on_tab_clicked("volume")

        # 2. 스크롤 영역 (기존과 동일)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background-color: transparent;")

        self.list_container = QWidget()
        self.list_container.setStyleSheet("background-color: transparent;")
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 0, 10)
        self.list_layout.setSpacing(8)
        self.list_layout.addStretch()  # 아래쪽 빈 공간 확보

        self.scroll.setWidget(self.list_container)
        self.main_layout.addWidget(self.scroll)

    def get_tab_style(self, active=False):
        """동그란 캡슐 모양 스타일 정의"""
        bg_color = PRIMARY if active else BORDER
        text_color = "white" if active else "#4E5968"
        font_weight = "bold" if active else "medium"

        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: 17px; /* 높이 35px의 절반 정도로 설정하여 완전 둥글게 */
                font-size: {FONT_SM}px;
                font-weight: {font_weight};
                border: none;
            }}
            QPushButton:hover {{
                background-color: {PRIMARY if active else SCROLLBAR};
            }}
        """

    def on_tab_clicked(self, tab_key):
        """탭 전환 시 스타일 업데이트"""
        for key, btn in self.tab_buttons.items():
            is_active = (key == tab_key)
            btn.setChecked(is_active)
            btn.setStyleSheet(self.get_tab_style(is_active))

        print(f"[{tab_key}] 데이터 로드 시퀀스 실행")

    def update_list(self, stock_data):
        # 기존 리스트 삭제 (위젯만 삭제하고 마지막 stretch는 유지)
        while self.list_layout.count() > 1:
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 새로운 데이터 추가
        for i, data in enumerate(stock_data, 1):
            item_widget = StockItemWidget(
                rank=i,
                name=data['name'],
                price=data['price'],
                change_rate=data['change_rate'],
                code=data['code']
            )
            self.list_layout.insertWidget(self.list_layout.count() - 1, item_widget)