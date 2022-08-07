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

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QInputDialog, QLineEdit, QMenu,
                               QMenuBar)

from QStyler.actions import (EditAction, LoadAction, ShowAction, opengithub,
                             saveQss)
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
        self.loadAction = LoadAction()
        self.loadAction.setText("Import Theme")
        self.fileMenu = FileMenu("File", parent=self)
        self.optionsMenu = ThemeMenu("Themes", parent=self)
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
        self.repolink = QAction("Open Github Repo")
        self.addAction(self.repolink)
        self.repolink.triggered.connect(opengithub)
        self.aboutQstyler = QAction("About QStyler")
        self.addAction(self.aboutQstyler)
        self.aboutQstyler.triggered.connect(self.open_about)

    def open_about(self):
        """Open the about QStyler Dialog."""


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
        self.titles = self.manager.titles
        self.resetAction = QAction("Reset Theme")
        self.saveCurrent = QAction("Save Theme As")
        self.resetAction.triggered.connect(self.manager.reset)
        toolbar = parent.window.styler.toolbar
        toolbar.loadAction = self.parent().loadAction
        self.parent().loadAction.loaded.connect(self.add_new_theme)
        self.themeMenu = QMenu("Themes", parent=self)
        self.saveCurrent.triggered.connect(self.createTheme)
        self.addAction(self.parent().loadAction)
        self.addAction(self.saveCurrent)
        self.addAction(self.resetAction)
        self.addMenu(self.themeMenu)
        self.themeactions = []
        for title in self.titles:
            action = QAction(title)
            action.key = title
            action.setObjectName(title + "action")
            action.triggered.connect(self.applyTheme)
            self.themeactions.append(action)
            self.themeMenu.addAction(action)
        self.themeMenu.addSeparator()

    def add_new_theme(self, theme, title):
        """Add new theme to the theme menu in menubar."""
        self.titles.append(title)
        action = QAction(title)
        action.key = title
        action.setObjectName(title + "action")
        action.triggered.connect(self.applyTheme)
        self.themeactions.append(action)
        self.themeMenu.addAction(action)
        self.manager.add_theme(theme, title)

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
        self.editAction = EditAction("Edit")
        self.saveAction = QAction("Save")
        self.showAction = ShowAction("Show StyleSheet")
        self.saveAction.triggered.connect(saveQss)
        self.exitAction.triggered.connect(exitApp)
        self.showAction.triggered.connect(self.showAction.showStyles)
        self.editAction.triggered.connect(self.editAction.edit_current_sheet)
        self.addAction(self.showAction)
        self.addAction(self.editAction)
        self.addAction(self.saveAction)
        self.addSeparator()
        self.addAction(self.exitAction)

    def applyStyleSheet(self):  # pragma: nocover
        """Apply theme to current app instance."""
        text = self.dialog.textEdit.toPlainText()
        parser = QssParser(text)
        self.parent().manager.sheets = parser.result
        self.parent.manager.set_sheet()
        self.dialog.close()
        self.dialog.deleteLater()
