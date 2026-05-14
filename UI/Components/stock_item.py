from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from UI.Styles.theme import *


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

        # 왼쪽: 순위와 이름 정보
        name_info_layout = QHBoxLayout()

        self.rank_label = QLabel(str(rank))
        self.rank_label.setFixedWidth(20)
        self.rank_label.setStyleSheet(f"font-size: {FONT_MD}px; font-weight: bold; color: {TEXT_MAIN};")

        self.name_label = QLabel(name)
        self.name_label.setStyleSheet(f"font-size: {FONT_MD}px; font-weight: 500; color: {TEXT_MAIN};")

        name_info_layout.addWidget(self.rank_label)
        name_info_layout.addWidget(self.name_label)

        # 오른쪽: 가격과 등락률
        price_info_layout = QVBoxLayout()
        price_info_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.price_label = QLabel(f"{price:,}원")
        self.price_label.setStyleSheet(f"font-size: {FONT_SM}px; font-weight: bold; color: {TEXT_MAIN};")

        # 등락률 색상 결정
        color = RED if "-" not in change_rate and change_rate != "0.00%" else BLUE
        self.change_label = QLabel(change_rate)
        self.change_label.setStyleSheet(f"font-size: {FONT_XS}px; color: {color};")

        price_info_layout.addWidget(self.price_label)
        price_info_layout.addWidget(self.change_label)

        layout.addLayout(name_info_layout)
        layout.addStretch()
        layout.addLayout(price_info_layout)

        # 스타일 설정
        self.setStyleSheet(f"""
            QFrame#StockItem {{
                background-color: white;
                border-radius: {RADIUS_ITEM}px;
            }}
            QFrame#StockItem:hover {{
                background-color: {HOVER};
            }}
        """)

    def mousePressEvent(self, event):
        self.clicked.emit(self.code)
        super().mousePressEvent(event)