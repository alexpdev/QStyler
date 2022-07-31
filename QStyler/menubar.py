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
        self.loadAction = QAction("Load Theme")
        self.loadAction.triggered.connect(self.loadTheme)
        self.resetAction.triggered.connect(self.resetStyleSheet)
        self.themeMenu = QMenu("Themes", parent=self)
        self.addMenu(self.themeMenu)
        self.addAction(self.loadAction)
        self.addAction(self.resetAction)
        self.themeactions = {}
        for key in self.themes:
            action = QAction(key)
            action.setObjectName(key + "action")
            action.triggered.connect(self.applyTheme)
            self.themeactions[action] = key
            self.themeMenu.addAction(action)
        self.themeMenu.addSeparator()

    def getThemeFile(self, title, path):
        """Open and save data in file path as title theme."""
        if path and title:
            parser = QssParser(path)
            theme = parser.result
            final = {}
            for row in theme:
                final.update(row)
            action = QAction(title)
            action.setObjectName(title + "action")
            self.themes[title] = final
            self.themeactions[action] = title
            self.themeMenu.addAction(action)
            action.triggered.connect(self.applyTheme)

    def loadTheme(self):  # pragma: nocover
        """Load a new theme into collection."""
        self.dialog = ThemeLoadDialog(self)
        self.dialog.closing.connect(self.getThemeFile)
        self.dialog.open()

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
        theme = {}
        for k, v in self.themeactions.items():
            if k == sender:
                theme = self.themes[v]
                break
        sheet = []
        for key, val in theme.items():
            sheet.append({key: val})
        self.manager.sheets = sheet
        self.manager.set_sheet()

    def resetStyleSheet(self):
        """Reset the current style sheet to blank."""

        self.manager.sheets = []
        sheet = self.manager.set_sheet()
        self.parent().window.setStyleSheet(sheet)
        self.parent().window.widgets.setStyleSheet(sheet)
        self.parent().window.styler.setStyleSheet(sheet)


class ThemeLoadDialog(QDialog):  # pragma: nocover
    """
    Open dialog to choose theme to load from qss file.

    Parameters
    ----------
    parent : QWidget
        This widgets parent widget.
    """

    closing = Signal([str, str])

    def __init__(self, parent=None):
        """
        Initialize the Load Theme dialog menu.

        Parameters
        ----------
        parent : QWidget, optional
            This Widgets Parent, by default None
        """
        super().__init__(parent=parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.label = QLabel("Theme Title", self)
        self.setWindowTitle("Load Theme")
        self.lineEdit = QLineEdit(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lineEdit)
        self.btn1 = QPushButton("Select File", self)
        self.btn2 = QPushButton("OK", self)
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.btn1)
        self.hlayout.addWidget(self.btn2)
        self.layout.addLayout(self.hlayout)
        self.label.setAlignment(Qt.AlignLeft)
        self.btn1.clicked.connect(self.loadTheme)
        self.btn2.clicked.connect(self.closeDialog)
        self.path = None

    def loadTheme(self):
        """Load new theme into database."""
        result = QFileDialog.getOpenFileName(self, "Select .qss File",
                                             str(Path().home()),
                                             "QSS(*.qss), Any(*)")
        if result[1]:
            self.path = result[0]
            name, _ = os.path.splitext(os.path.basename(self.path))
            self.lineEdit.setText(name)

    def closeDialog(self):
        """Close dialog and return file path if selected."""
        text = self.lineEdit.text()
        path = self.path if self.path else ""
        self.closing.emit(text, path)
        self.close()


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
