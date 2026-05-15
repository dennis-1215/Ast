import sys
from PySide6.QtWidgets import QApplication
from UI.trading_app import TradingApp

app = QApplication(sys.argv)

window = TradingApp()
window.show()

sys.exit(app.exec())