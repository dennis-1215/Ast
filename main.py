import sys
from PySide6.QtWidgets import QApplication
from mainPage import *

app = QApplication(sys.argv)

window = TradingApp()
window.show()

sys.exit(app.exec())