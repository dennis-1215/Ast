from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QStackedWidget
)

from UI.Pages.home_page import HomePage
from UI.Styles.theme import *


class TradingApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stock Trading Program")
        self.resize(1280, 800)
        self.setStyleSheet(
            f"""
            background-color: {BACKGROUND};
            """
        )

        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 페이지 스택
        self.page_stack = QStackedWidget()
        self.main_layout.addWidget(self.page_stack,1)

        # 페이지 생성
        self.home_page = HomePage()

        # 페이지 등록
        self.page_stack.addWidget(self.home_page)