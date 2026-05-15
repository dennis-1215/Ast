from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt, Signal

from UI.Styles.theme import *


class BaseStockItem(QFrame):

    clicked = Signal(str)

    def __init__(self, code=None):
        super().__init__()

        self.code = code

        self.setObjectName("StockItem")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setStyleSheet(f"""
            QFrame#StockItem {{
                background-color: rgba(255,255,255,0.85);
                border-radius: {RADIUS_ITEM}px;
            }}

            QFrame#StockItem:hover {{
                background-color: white;
            }}
        """)

    def mousePressEvent(self, event):
        if self.code:
            self.clicked.emit(self.code)

        super().mousePressEvent(event)