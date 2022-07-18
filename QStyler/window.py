#! /usr/bin/python3
# -*- coding: utf-8 -*-

##############################################################################
#  Copyright 2022 alexpdev
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
##############################################################################
"""Module for creating the main window for the application."""

import sys
from typing import Optional

from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget,
                               QVBoxLayout, QWidget)

from QStyler.menubar import MenuBar
from QStyler.styler import StylerTab
from QStyler.utils import get_icon
from QStyler.widgets import WidgetsTab


class MainWindow(QMainWindow):
    """
    Create the main window widget for the application.

    Parameters
    ----------
    parent : widget or None
        The widgets parent.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Initialize main window."""
        super().__init__(parent=parent)
        self.setWindowTitle("QStyler")
        self.central = QWidget(parent=self)
        self.layout = QVBoxLayout()
        self.central.setLayout(self.layout)
        self.setCentralWidget(self.central)
        self.setObjectName("MainWindow")
        self.resize(700, 600)
        self.tabWidget = QTabWidget()
        self.setWindowIcon(get_icon("QStylerIcon.png"))
        self.widgets = WidgetsTab(parent=self)
        self.styler = StylerTab(parent=self)
        self.tabWidget.addTab(self.widgets, "Widgets")
        self.tabWidget.addTab(self.styler, "Style")
        self.layout.addWidget(self.tabWidget)
        self.menubar = MenuBar(self)
        self.setMenuBar(self.menubar)


def execute():  # pragma: nocover
    """Entry point for cli and execution."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
