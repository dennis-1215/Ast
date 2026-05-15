from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout
)
from PySide6.QtCore import Qt

from UI.Components.base_stock_item import BaseStockItem
from UI.Styles.theme import *


class AssetStockItem(BaseStockItem):
    def __init__(self, stock):
        super().__init__(stock["code"])

        self.setFixedHeight(65)

        name = stock["name"]
        qty = stock["qty"]
        profit_rt = stock["profit_rt"]

        # 수익률 색상
        color = (
            RED if profit_rt > 0
            else BLUE if profit_rt < 0
            else "#4E5968"
        )

        # 메인 레이아웃
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)

        # 왼쪽 영역
        left_layout = QVBoxLayout()
        left_layout.setSpacing(2)

        self.name_label = QLabel(name)
        self.name_label.setStyleSheet(
            f"""
            font-size: {FONT_MD}px;
            font-weight: 600;
            color: {TEXT_MAIN};
            """
        )

        self.qty_label = QLabel(f"{qty}주 보유")
        self.qty_label.setStyleSheet(
            f"""
            font-size: {FONT_XS}px;
            color: {TEXT_SUB};
            """
        )

        left_layout.addWidget(self.name_label)
        left_layout.addWidget(self.qty_label)

        # 오른쪽 영역
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        right_layout.setSpacing(2)

        current_value = stock["current_value"]
        profit_amount = stock["profit_amount"]

        # 현재 평가 금액
        self.value_label = QLabel(f"₩{current_value:,}")
        self.value_label.setStyleSheet(
            f"""
            font-size: {FONT_SM}px;
            font-weight: bold;
            color: {TEXT_MAIN};
            """
        )

        # 수익 텍스트
        profit_prefix = "+" if profit_amount > 0 else ""

        self.profit_label = QLabel(
            f"{profit_prefix}₩{profit_amount:,} ({profit_rt:.2f}%)"
        )

        self.profit_label.setStyleSheet(
            f"""
            font-size: {FONT_XS}px;
            font-weight: bold;
            color: {color};
            """
        )

        right_layout.addWidget(
            self.value_label,
            alignment=Qt.AlignmentFlag.AlignRight
        )

        right_layout.addWidget(
            self.profit_label,
            alignment=Qt.AlignmentFlag.AlignRight
        )

        # 합치기
        layout.addLayout(left_layout)
        layout.addStretch()
        layout.addLayout(right_layout)