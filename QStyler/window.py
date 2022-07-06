import sys
import os
from typing import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QCommandLinkButton, QDateEdit, QDateTimeEdit, QDial,
    QDialogButtonBox, QDoubleSpinBox, QFontComboBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLCDNumber, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMenuBar, QPlainTextEdit,
    QProgressBar, QPushButton, QRadioButton, QScrollArea,
    QScrollBar, QSizePolicy, QSlider, QSpinBox,
    QStackedWidget, QStatusBar, QTabWidget, QTableWidget,
    QTableWidgetItem, QTextBrowser, QTextEdit, QTimeEdit,
    QToolBox, QToolButton, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

from QStyler.tab1 import Tab1
from QStyler.tab2 import Tab2


class MainWindow(QMainWindow):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        self.central = QWidget(parent=self)
        self.layout = QGridLayout()
        self.central.setLayout(self.central)
        self.setCentralWidget(self.central)
        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.tabWidget = QTabWidget(self.central)
        self.tab = Tab1()
        self.tab_2 = Tab2()
        self.tabWidget.addTab(self.tab, "tab1")
        self.tabWidget.addTab(self.tab_2, "tab2")
