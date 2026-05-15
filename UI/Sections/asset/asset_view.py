from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from UI.Components.asset_list_panel import AssetListPanel
from UI.Styles.theme import *

class AssetView(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)

        # =========================
        # 2. 총 자산
        # =========================
        self.asset_label = QLabel("0 ₩")
        self.asset_label.setStyleSheet(f"""
            font-size: 24px;
            font-weight: 800;
            color: {TEXT_MAIN};
            background-color: white;
        """)

        self.layout.addWidget(self.asset_label)

        # =========================
        # 3. 수익률 뱃지 영역
        # =========================
        self.badge_container = QHBoxLayout()

        self.profit_badge = QLabel("-")
        self.profit_badge.setStyleSheet(f"""
            background-color: #F2F4F6;
            color: #4E5968;
            font-weight: bold;
            padding: 6px 10px;
            border-radius: 8px;
        """)

        self.badge_container.addWidget(self.profit_badge)
        self.badge_container.addStretch()

        self.layout.addLayout(self.badge_container)

        # =========================
        # 4. 리스트
        # =========================
        self.asset_list = AssetListPanel()
        self.layout.addWidget(self.asset_list, 1)

    # =========================
    # UPDATE FUNCTIONS (MVC 유지)
    # =========================
    def set_asset_summary(self, total_asset):
        self.asset_label.setText(f"{total_asset:,} ₩")

    def set_profit_badge(self, text, style):
        self.profit_badge.setText(text)
        self.profit_badge.setStyleSheet(style)

    def set_stocks(self, stocks):
        self.asset_list.update_stocks(stocks)