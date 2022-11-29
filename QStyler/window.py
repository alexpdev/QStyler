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

from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget

from QStyler.collectionsTab import CollectionsTab
from QStyler.editorTab import EditorsTab
from QStyler.menubar import MenuBar
from QStyler.styler import StylerTab
from QStyler.utils import StyleManager, get_icon, get_manager
from QStyler.widgets import WidgetsTab


class MainWindow(QMainWindow):
    """
    Create the main window widget for the application.

    Parameters
    ----------
    parent : widget or None
        The widgets parent.
    """

    manager = None

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Initialize main window."""
        super().__init__(parent=parent)
        self.setWindowTitle("QStyler")
        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)
        self.setObjectName("MainWindow")
        self.resize(900, 700)
        self.setWindowIcon(get_icon("QStylerIcon.png"))
        self.manager = get_manager()
        self.menubar = MenuBar(self)
        self.statusbar = self.statusBar()
        self.setMenuBar(self.menubar)
        self.add_widgets()

    def add_widgets(self):
        """Add widgets to the main window."""
        self.styler = StylerTab(parent=self)
        self.widgets = WidgetsTab(parent=self)
        self.editors = EditorsTab(parent=self)
        self.collections = CollectionsTab(parent=self)
        self.tabWidget.addTab(self.styler, "Style")
        self.tabWidget.addTab(self.widgets, "Widgets")
        self.tabWidget.addTab(self.editors, "Editors")
        self.tabWidget.addTab(self.collections, "Collections")
        self.styler.toolbar.activate_load_item()


class Application(QApplication):
    """Subclass of the QApplication."""

    def __init__(self, args=None, windowclass=MainWindow):
        """Initialize application."""
        if not args:
            args = sys.argv  # pragma: nocover
        super().__init__(args)
        self.manager = StyleManager()
        self.window = windowclass()


def execute():  # pragma: nocover
    """Entry point for cli and execution."""
    app = Application(sys.argv, MainWindow)
    app.window.show()
    sys.exit(app.exec())
