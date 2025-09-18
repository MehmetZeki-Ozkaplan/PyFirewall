import sys
from PyQt5.QtWidgets import QApplication
from ui.firewall_gui import FirewallGUI
from resources.theme import DARK_THEME

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME)
    window = FirewallGUI()
    window.show()
    sys.exit(app.exec_())
