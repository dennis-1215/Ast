from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel
)


class BaseCard(QFrame):

    def __init__(
            self,
            title="",
            padding=20,
            radius=20,
            parent=None
    ):
        super().__init__(parent)

        self.setObjectName("baseCard")

        self.setStyleSheet(f"""
            QFrame#baseCard {{
                background-color: white;
                border-radius: {radius}px;
            }}
        """)

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            padding,
            padding,
            padding,
            padding
        )

        self.main_layout.setSpacing(10)

        # 제목
        if title:

            self.title_label = QLabel(title)

            self.title_label.setStyleSheet("""
                font-size: 20px;
                font-weight: 800;
                color: #191F28;
                background-color: transparent;
            """)

            self.main_layout.addWidget(
                self.title_label
            )

    def layout(self):
        return self.main_layout