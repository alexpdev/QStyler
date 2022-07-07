import sys
import os
from typing import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from QStyler.tab1 import Tab1
from QStyler.tab2 import Tab2


class MainWindow(QMainWindow):

    def __init__(self, app: Optional[QApplication] = None,
                       parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        self.app = app
        self.central = QWidget(parent=self)
        self.layout = QVBoxLayout()
        self.central.setLayout(self.layout)
        self.setCentralWidget(self.central)
        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.tabWidget = QTabWidget(self.central)
        self.tab = Tab1(parent=self)
        self.tab_2 = Tab2(parent=self)
        self.tabWidget.addTab(self.tab, "Styles")
        self.tabWidget.addTab(self.tab_2, "Widgets")
        self.layout.addWidget(self.tabWidget)
