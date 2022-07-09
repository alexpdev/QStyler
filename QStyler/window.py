import sys
import os
from typing import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from QStyler.tab1 import Tab1
from QStyler.tab2 import Tab2
from QStyler.menubar import MenuBar


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
        self.tabWidget = QTabWidget()
        self.tab = Tab1(parent=self)
        self.widget2 = Tab2(parent=self)
        self.tabWidget.addTab(self.tab, "Styles")
        self.tabWidget.addTab(QWidget(), "Blank")
        self.layout.addWidget(self.tabWidget)
        self.layout.addWidget(self.widget2)
        self.menubar = MenuBar(self)
        self.setMenuBar(self.menubar)
