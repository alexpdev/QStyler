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
import webbrowser
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog, QHBoxLayout,
                               QInputDialog, QLabel, QLineEdit, QMenu,
                               QMenuBar, QPlainTextEdit, QPushButton,
                               QTextBrowser, QVBoxLayout, QWidget)

from QStyler.utils import QssParser, exitApp, get_manager
from QStyler.actions import LoadAction


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
        self.manager = get_manager()
        self.fileMenu = FileMenu("File", parent=self)
        self.optionsMenu = ThemeMenu("Theme", parent=self)
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
        self.repolink = QAction("Github Repo")
        self.addAction(self.repolink)
        self.repolink.triggered.connect(self.opengithub)

    @staticmethod
    def opengithub():  # pragma: nocover
        """Open webbrowser to github repo."""
        webbrowser.open("https://github.com/alexpdev/QStyler")


class ThemeMenu(QMenu):
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
        self.manager = get_manager()
        self.themes = self.manager.themes
        self.resetAction = QAction("Reset Theme")
        self.loadAction = LoadAction("Load Theme")
        self.saveCurrent = QAction("Save Current Theme")
        self.resetAction.triggered.connect(self.manager.reset)
        self.loadAction.loaded.connect(self.add_new_theme)
        self.themeMenu = QMenu("Themes", parent=self)
        self.saveCurrent.triggered.connect(self.createTheme)
        self.addAction(self.loadAction)
        self.addAction(self.saveCurrent)
        self.addMenu(self.themeMenu)
        self.addAction(self.resetAction)
        self.themeactions = []
        for key in self.themes:
            action = QAction(key)
            action.key = key
            action.setObjectName(key + "action")
            action.triggered.connect(self.applyTheme)
            self.themeactions.append(action)
            self.themeMenu.addAction(action)
        self.themeMenu.addSeparator()

    def add_new_theme(self, theme, title):
        """Add new theme to the theme menu in menubar."""
        self.themes[title] = theme
        action = QAction(title)
        action.key = title
        action.setObjectName(title + "action")
        action.triggered.connect(self.applyTheme)
        self.themeactions.append(action)
        self.themeMenu.addAction(action)

    def createTheme(self):  # pragma: nocover
        """Save the current stylesheet as a theme to use in the future."""
        sheets = self.manager.sheets
        name, status = QInputDialog.getText(self, "Enter Theme Name",
                                            "Theme Name", QLineEdit.Normal, "")
        if status and name not in self.themes:
            theme = {}
            map(theme.update, sheets)
            self.themes[name] = theme
            json.dump(self.themes, open(self.path, "wt", encoding="utf-8"))
        return True

    def applyTheme(self):
        """Apply chosen theme to mainwindow and application."""
        sender = self.sender()
        title = sender.key
        self.manager.apply_theme(title)


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
        self.editAction = QAction("Edit")
        self.saveAction = QAction("Save")
        self.showAction = QAction("Show StyleSheet")
        self.saveAction.triggered.connect(self.saveQss)
        self.exitAction.triggered.connect(exitApp)
        self.showAction.triggered.connect(self.showStyles)
        self.editAction.triggered.connect(self.editCurrentSheet)
        self.addAction(self.showAction)
        self.addAction(self.editAction)
        self.addAction(self.saveAction)
        self.addSeparator()
        self.addAction(self.exitAction)
        self.parent().window.styler.button.clicked.connect(self.showStyles)

    def showStyles(self):  # pragma: nocover
        """Show the current stylesheet in a separate widget."""
        sheet = QApplication.instance().styleSheet()
        self.dialog = QWidget()
        self.dialog.resize(300, 200)
        layout = QVBoxLayout()
        self.dialog.setLayout(layout)
        self.dialog.setWindowTitle("Current Style Sheet")
        textEdit = QTextBrowser(parent=self.dialog)
        textEdit.setPlainText(sheet)
        layout.addWidget(textEdit)
        self.dialog.show()
        button = QPushButton("Save", parent=self)
        layout.addWidget(button)
        button.clicked.connect(self.saveQss)

    def saveQss(self):  # pragma: nocover
        """Save current style to file."""
        path = QFileDialog.getSaveFileName(self, "Save File", str(Path.home()),
                                           "QSS (*.qss); Any (*)")
        if path:
            with open(path, "wt", encoding="utf-8") as fd:
                sheet = QApplication.instance().styleSheet()
                fd.write(sheet)
        return True

    def editCurrentSheet(self):  # pragma: nocover
        """Edit the current sheet."""
        sheet = QApplication.instance().styleSheet()
        self.dialog = QWidget()
        self.dialog.resize(400, 280)
        layout = QVBoxLayout()
        self.dialog.setLayout(layout)
        textEdit = QPlainTextEdit(self.dialog)
        self.dialog.setWindowTitle("StyleSheet Editor")
        layout.addWidget(textEdit)
        savebtn = QPushButton("Apply", parent=self.dialog)
        cancelbtn = QPushButton("Cancel", parent=self.dialog)
        savebtn.pressed.connect(self.applyStyleSheet)
        cancelbtn.pressed.connect(self.closeDialog)
        hlayout = QHBoxLayout()
        hlayout.addWidget(savebtn)
        hlayout.addWidget(cancelbtn)
        layout.addLayout(hlayout)
        textEdit.setPlainText(sheet)
        self.dialog.show()

    def closeDialog(self):  # pragma: nocover
        """Exit dialog window."""
        self.dialog.close()
        self.dialog.deleteLater()

    def applyStyleSheet(self):  # pragma: nocover
        """Apply theme to current app instance."""
        text = self.dialog.textEdit.toPlainText()
        parser = QssParser(text)
        self.parent().manager.sheets = parser.result
        self.parent.manager.set_sheet()
        self.dialog.close()
        self.dialog.deleteLater()
