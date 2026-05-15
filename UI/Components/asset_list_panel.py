from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QScrollArea
)
from PySide6.QtCore import Qt

from UI.Components.asset_stock_item import AssetStockItem
from UI.Styles.theme import *


class AssetListPanel(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 배경 프레임
        self.list_frame = QFrame()
        self.list_frame.setStyleSheet(
            f"""
            background-color: {BORDER};
            border-radius: {RADIUS_CARD}px;
            """
        )

        frame_layout = QVBoxLayout(self.list_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)

        # 스크롤 영역
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        #self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
                border-radius: 12px;
            }
        
            QScrollBar:vertical {
                width: 10px;
                background: transparent;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #c1c1c1;
                border-radius: 5px;
            }
            QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical {
                height: 0px;
            }
            """
        )

        # 스크롤 내부 위젯
        self.scroll_widget = QWidget()

        self.stock_list_layout = QVBoxLayout(self.scroll_widget)
        self.stock_list_layout.setContentsMargins(15, 15, 15, 15)
        self.stock_list_layout.setSpacing(8)
        self.stock_list_layout.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidget(self.scroll_widget)

        frame_layout.addWidget(self.scroll_area)

        main_layout.addWidget(self.list_frame)

    def update_stocks(self, stocks):
        self.clear()

        if not stocks:
            self.show_empty()
            return

        for stock in stocks:
            item = AssetStockItem(stock)
            self.stock_list_layout.addWidget(item)

        self.stock_list_layout.addStretch()

    def clear(self):
        while self.stock_list_layout.count():
            item = self.stock_list_layout.takeAt(0)

            widget = item.widget()
            if widget:
                widget.deleteLater()

    def show_empty(self):
        empty_label = QLabel("보유한 종목이 없습니다")

        empty_label.setAlignment(Qt.AlignCenter)

        empty_label.setStyleSheet(
            """
            font-family: 'Pretendard';
            color: #444444;
            font-size: 18px;
            font-weight: 600;
            """
        )

        empty_label.setMinimumHeight(320)

        self.stock_list_layout.addWidget(empty_label)