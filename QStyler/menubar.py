import sys
import os
from typing import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class MenuBar(QMenuBar):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.window = parent
        self.fileMenu = QMenu("File")
        self.editMenu = QMenu("Edit")
        self.helpMenu = QMenu("Help")
        self.optionsMenu = QMenu("Options")
        self.addMenu(self.fileMenu)
        self.addMenu(self.editMenu)
        self.addMenu(self.optionsMenu)
        self.addMenu(self.helpMenu)
        self.exitAction = QAction("Exit")
        self.fileMenu.addAction(self.exitAction)
