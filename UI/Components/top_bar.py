from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel
)

from PySide6.QtCore import Qt

from UI.Components.search_bar import SearchBar
from UI.Components.news_ticker import NewsTicker

from UI.Utils.image_utils import ImageUtils

from UI.Styles.theme import *


class TopBar(QWidget):

    def __init__(self, news_data):
        super().__init__()

        self.news_data = news_data
        self.setFixedHeight(70)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(25, 15, 25, 0)
        main_layout.setSpacing(5)

        # 왼쪽 영역
        left_container = self.create_left_section()

        # 중앙 영역
        center_container = self.create_center_section()

        # 오른쪽 영역
        right_container = self.create_right_section()

        main_layout.addWidget(left_container, 1)
        main_layout.addWidget(center_container, 1)
        main_layout.addWidget(right_container, 1)

    def create_left_section(self):

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # 로고 이미지
        logo_icon = QLabel()
        logo_icon.setPixmap(
            ImageUtils.load_pixmap(
                "Logo.png",
                60,
                60
            )
        )

        layout.addWidget(logo_icon)

        # 텍스트 영역
        text_layout = QVBoxLayout()

        text_layout.setContentsMargins(0, 13, 0, 13)

        self.logo_title = QLabel("STOCK TRADING PROGRAM")

        self.logo_title.setStyleSheet(
            f"""
            font-weight: bold;
            color: #333D4B;
            font-size: {FONT_SM};
            """
        )

        self.time_label = QLabel()
        self.time_label.setStyleSheet(
            f"""
            color: #4E5968;
            font-size: {FONT_XS};
            """
        )

        text_layout.addWidget(self.logo_title)
        text_layout.addWidget(self.time_label)
        layout.addLayout(text_layout)

        return container

    def create_center_section(self):

        container = QWidget()

        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        self.search_bar = SearchBar(placeholder="삼성전자, 005930, 테마 검색")
        layout.addWidget(self.search_bar)

        return container

    def create_right_section(self):

        container = QWidget()

        layout = QHBoxLayout(container)
        layout.setContentsMargins(50, 0, 0, 0)
        layout.setAlignment(Qt.AlignLeft)

        self.news_ticker = NewsTicker()
        self.news_ticker.set_news(self.news_data)
        layout.addWidget(self.news_ticker)

        return container

    def update_clock(self, text):
        self.time_label.setText(text)
