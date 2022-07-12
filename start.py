import sys
from QStyler import MainWindow
from PySide6.QtWidgets import QApplication

def start():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app, window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
