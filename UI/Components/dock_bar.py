from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QFrame
)

from PySide6.QtCore import Qt, Signal

from UI.Styles.theme import *


class DockBar(QWidget):

    menu_clicked = Signal(str)

    def __init__(self):
        super().__init__()

        self.buttons = {}

        self.setFixedHeight(100)

        main_layout = QHBoxLayout(self)

        # 실제 dock
        self.dock_bar = QFrame()
        self.dock_bar.setFixedSize(500, 70)
        self.dock_bar.setStyleSheet(
            f"""
            background-color: white;
            border-radius: 35px;
            border: 1px solid {BORDER};
            """
        )

        menu_layout = QHBoxLayout(self.dock_bar)
        menu_layout.setContentsMargins(20, 0, 20, 0)

        menus = [
            ("home", "🏠", "홈"),
            ("favorite", "⭐", "즐겨찾기"),
            ("strategy", "💡", "매매전략"),
            ("analysis", "📊", "전략분석")
        ]

        for key, icon, name in menus:

            button = QPushButton(f"{icon}\n{name}")
            button.setCursor(Qt.PointingHandCursor)

            button.clicked.connect(
                lambda checked=False, k=key:
                self.on_menu_clicked(k)
            )

            button.setStyleSheet(self.get_button_style())
            menu_layout.addWidget(button)

            self.buttons[key] = button

        main_layout.addWidget(
            self.dock_bar,
            0,
            Qt.AlignCenter
        )

        self.set_active("home")

    def on_menu_clicked(self, key):

        self.set_active(key)

        self.menu_clicked.emit(key)

    def set_active(self, active_key):

        for key, button in self.buttons.items():

            if key == active_key:
                button.setStyleSheet(
                    self.get_button_style(active=True)
                )

            else:
                button.setStyleSheet(
                    self.get_button_style(active=False)
                )

    def get_button_style(self, active=False):

        if active:
            return f"""
                QPushButton {{
                    background-color: {PRIMARY};
                    color: white;
                    border-radius: 18px;
                    font-size: 11px;
                    font-weight: bold;
                    border: none;
                    padding: 6px;
                }}
            """

        return f"""
            QPushButton {{
                background-color: transparent;
                color: #4E5968;
                border-radius: 18px;
                font-size: 11px;
                font-weight: bold;
                border: none;
                padding: 6px;
            }}

            QPushButton:hover {{
                background-color: {HOVER};
            }}
        """