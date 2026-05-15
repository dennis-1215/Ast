# 조립기다
# View, Controller, Model 들을 조립해서 완전한 페이지를 제공한다.

from PySide6.QtWidgets import QWidget, QVBoxLayout

from UI.Components.base_card import BaseCard

from UI.Sections.asset.asset_view import AssetView
from UI.Sections.asset.asset_controller import AssetController

class AssetSection(QWidget):

    def __init__(self, service):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.card = BaseCard("My Assets (내 자산)")

        self.view = AssetView()

        self.controller = AssetController(service, self.view)

        self.card.layout().addWidget(self.view)

        layout.addWidget(self.card)

    def refresh(self):
        self.controller.refresh()