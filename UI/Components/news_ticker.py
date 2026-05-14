import webbrowser

from PySide6.QtWidgets import (QFrame, QLabel, QHBoxLayout)
from PySide6.QtCore import Qt

from UI.Styles.theme import *


class NewsTicker(QFrame):
    def __init__(self, width=320, parent=None):
        super().__init__(parent)
        self.news_data = []
        self.current_index = 0
        self.fixed_width = width
        self.init_ui()

    def init_ui(self):
        self.setObjectName("NewsTicker")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(50, 0, 0, 0)
        layout.setAlignment(Qt.AlignLeft)

        # 뉴스 라벨
        self.news_label = QLabel("뉴스를 불러오는 중...")
        self.news_label.setFixedWidth(self.fixed_width)
        self.news_label.setWordWrap(True)
        self.news_label.setCursor(Qt.PointingHandCursor)

        self.news_label.setStyleSheet(f"""
            QLabel {{
                color: #4E5968;
                font-size: 13px;
                border: none;
                background: transparent;
                qproperty-alignment:
                    'AlignLeft | AlignVCenter';
            }}

            QLabel:hover {{
                text-decoration: underline;
                color: {BLUE};
            }}
        """)

        # 클릭 이벤트
        self.news_label.mousePressEvent = (self.on_news_clicked)
        layout.addWidget(self.news_label)

    # 뉴스 데이터 설정
    def set_news(self, news_list):

        self.news_data = news_list
        self.current_index = 0

        self.update_news()

    # 현재 뉴스 업데이트
    def update_news(self):
        if not self.news_data:
            self.news_label.setText("표시할 뉴스가 없습니다")
            return

        current_news = self.news_data[self.current_index]
        title = current_news.get("title", "제목 없음")
        self.news_label.setText(title)

    # 다음 뉴스
    def next_news(self):

        if not self.news_data:
            return

        self.current_index += 1

        if self.current_index >= len(self.news_data):
            self.current_index = 0

        self.update_news()

    # 현재 뉴스 URL 열기
    def open_current_news(self):
        if not self.news_data:
            return

        current_news = self.news_data[self.current_index]
        url = current_news.get("url")
        if url:
            webbrowser.open(url)

    # 클릭 이벤트
    def on_news_clicked(self, event):
        self.open_current_news()