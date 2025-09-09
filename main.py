import sys
from PyQt6.QtWidgets import QApplication
from gui import MainWindow
from gui.stylesheets import get_dark_theme

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(get_dark_theme())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
