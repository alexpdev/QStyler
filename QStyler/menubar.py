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
"""Module for initializing the menubar."""

import json
import os
from pathlib import Path

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QFileDialog, QInputDialog,
                               QLineEdit, QMenu, QMenuBar, QPushButton,
                               QTextBrowser, QVBoxLayout, QWidget)

from QStyler.utils import exitApp


class MenuBar(QMenuBar):
    """
    Create a mainwindow menu bar for the default menubar.

    Parameters
    ----------
    parent : QWidget
        This widgets parent.
    """

    def __init__(self, parent) -> None:
        """
        Initialize menubar.

        Parameters
        ----------
        parent : QWidget, optional
            the parent of the widget, by default None
        """
        super().__init__(parent)
        self.window = parent
        self.fileMenu = FileMenu("File", parent=self)
        self.optionsMenu = OptionsMenu("Options", parent=self)
        self.helpMenu = HelpMenu("Help", parent=self)
        self.addMenu(self.fileMenu)
        self.addMenu(self.optionsMenu)
        self.addMenu(self.helpMenu)


class HelpMenu(QMenu):
    """
    Creates Edit menu for the mainwindow menu bar.

    Parameters
    ----------
    text : str
        The text displayed on the menubar
    parent : QWidget
        This widgets parent widget
    """

    def __init__(self, text: str, parent=None) -> None:
        """
        Create the menu widget.

        Parameters
        ----------
        text : str
            menu bar text
        parent : QWidget, optional
            this widgets parent, by default None
        """
        super().__init__(text, parent=parent)
        self.aboutqt = QAction("About Qt")
        self.addAction(self.aboutqt)
        self.aboutqt.triggered.connect(QApplication.instance().aboutQt)


class OptionsMenu(QMenu):
    """
    Creates options menu for the mainwindow menu bar.

    Parameters
    ----------
    text : str
        The text displayed on the menubar
    parent : QWidget
        This widgets parent widget
    """

    def __init__(self, text: str, parent=None) -> None:
        """
        Initialize menu.

        Parameters
        ----------
        text : str
            Title of menu.
        parent : QWidget, optional
            the parent of the widget, by default None
        """
        super().__init__(text, parent=parent)
        self.path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "style", "themes.json"
        )
        self.themes = json.load(open(self.path, encoding="utf-8"))
        self.resetAction = QAction("Reset")
        self.addAction(self.resetAction)
        self.createThemeAction = QAction("Create Theme")
        self.createThemeAction.triggered.connect(self.createTheme)
        self.resetAction.triggered.connect(self.resetStyleSheet)
        self.addAction(self.createThemeAction)
        self.themeMenu = QMenu("Themes", parent=self)
        self.addMenu(self.themeMenu)
        self.themeactions = {}
        for key in self.themes:
            action = QAction(key)
            action.setObjectName(key + "action")
            action.triggered.connect(self.applyTheme)
            self.themeactions[action] = key
            self.themeMenu.addAction(action)

    def createTheme(self):  # pragma: nocover
        """
        Save the current stylesheet as a theme to use in the future.
        """
        sheets = self.parent().window.styler.table.factory.sheets
        name, status = QInputDialog.getText(
            self, "Enter Theme Name", "Theme Name", QLineEdit.Normal, ""
        )
        if status and name not in self.themes:
            theme = {}
            map(theme.update, sheets)
            self.themes[name] = theme
            json.dump(self.themes, open(self.path, "wt", encoding="utf-8"))
        return True

    def applyTheme(self):
        """Apply chosen theme to mainwindow and application."""
        sender = self.sender()
        theme = {}
        for k, v in self.themeactions.items():
            if k == sender:
                theme = self.themes[v]
                break
        sheet = []
        for key, val in theme.items():
            sheet.append({key: val})
        self.parent().window.styler.table.factory.sheets = sheet
        self.parent().window.styler.table.factory.update_styleSheet()

    def resetStyleSheet(self):
        """Reset the current style sheet to blank."""
        parent = self.parent()
        parent.window.styler.table.factory.sheets = []
        sheet = parent.window.styler.table.factory.update_styleSheet()
        self.parent().window.setStyleSheet(sheet)
        parent.window.widgets.setStyleSheet(sheet)
        parent.window.styler.setStyleSheet(sheet)


class FileMenu(QMenu):
    """
    Creates file menu for the mainwindow menu bar.

    Parameters
    ----------
    text : str
        The text displayed on the menubar
    parent : QWidget
        This widgets parent widget
    """

    def __init__(self, text: str, parent=None) -> None:
        """
        Initialize menu.

        Parameters
        ----------
        text : str
            Title of menu.
        parent : QWidget, optional
            the parent of the widget, by default None
        """
        super().__init__(text, parent=parent)
        self.exitAction = QAction("Exit")
        self.showAction = QAction("Show StyleSheet")
        self.exitAction.triggered.connect(exitApp)
        self.showAction.triggered.connect(self.showStyles)
        self.addAction(self.showAction)
        self.addAction(self.exitAction)

    def showStyles(self):  # pragma: nocover
        """Show the current stylesheet in a separate widget."""
        sheet = QApplication.instance().styleSheet()
        self.dialog = QWidget()
        self.dialog.resize(300, 200)
        layout = QVBoxLayout()
        self.dialog.setLayout(layout)
        textEdit = QTextBrowser(parent=self.dialog)
        textEdit.setPlainText(sheet)
        layout.addWidget(textEdit)
        self.dialog.show()
        button = QPushButton("Save", parent=self)
        layout.addWidget(button)
        button.clicked.connect(self.saveQss)

    def saveQss(self):  # pragma: nocover
        """Save current style to file."""
        path = QFileDialog.getSaveFileName(
            self, "Save File", str(Path.home()), "QSS (*.qss); Any (*)"
        )
        if path:
            with open(path, "wt", encoding="utf-8") as fd:
                sheet = QApplication.instance().styleSheet()
                fd.write(sheet)
        return True
