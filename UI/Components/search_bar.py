from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit
)
from PySide6.QtCore import Qt, Signal

from UI.Utils.image_utils import ImageUtils

class SearchBar(QFrame):
    # 엔터 입력시 검색어 전달
    search_requested = Signal(str)

    def __init__(self, placeholder="종목 검색", width=470, height=40, parent=None):
        super().__init__(parent)

        self.setFixedSize(width, height)

        self.setStyleSheet("""
            SearchBar {
                background-color: white;
                border-radius: 20px;
                border : 1px solid #E5E8EB;
            }
        """)

        self.init_ui(placeholder)

    def init_ui(self, placeholder):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(10)

        # 검색 아이콘 추가
        self.search_icon = QLabel()
        self.search_icon.setPixmap(ImageUtils.load_pixmap("search.png", 20, 20))
        self.search_icon.setStyleSheet("border: none; background-color: transparent;")

        # 입력창
        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        self.input.setStyleSheet("""
                    border: none;
                    background: transparent;
                    font-size: 14px;
                    color: #191F28;
                """)

        # 엔터 이벤트
        self.input.returnPressed.connect(self.emit_search)

        layout.addWidget(self.search_icon)
        layout.addWidget(self.input)

    # 검색 이벤트
    def emit_search(self):
        text = self.input.text().strip()
        if text:
            self.search_requested.emit(text)

    # 외부에서 텍스트 가져오기
    def text(self):
        return self.input.text()

    # 외부에서 텍스트 설정
    def set_text(self, text):
        self.input.setText(text)

    # 입력창 비우기
    def clear(self):
        self.input.clear()