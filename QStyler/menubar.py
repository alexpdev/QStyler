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

from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMenu, QMenuBar

from QStyler.utils import exitApp
from QStyler.dialog import AboutQStyler


class MenuBar(QMenuBar):
    """
    Create a mainwindow menu bar for the default menubar.

    Parameters
    ----------
    parent : QWidget
        This widgets parent.
    """

    displayStyles = Signal()

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
        self.fileMenu.displayStyles.connect(self.displayStyles)
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
        self.aboutQstyler = QAction("About QStyler")
        self.addAction(self.aboutQstyler)
        self.aboutQstyler.triggered.connect(self.open_about)

    def open_about(self):
        """Open the about QStyler Dialog."""
        self.dialog = AboutQStyler(self)
        self.dialog.exec()


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

    resetClicked = Signal()
    saveCurrentClicked = Signal()
    loadThemeClicked = Signal()
    previewThemeClicked = Signal()

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
        self.resetAction = QAction("Reset Theme")
        self.saveCurrent = QAction("Save Theme As")
        self.loadTheme = QAction("Load Theme")
        self.previewTheme = QAction("Preview Theme")
        self.themeMenu = QMenu("Themes", parent=self)
        self.addAction(self.resetAction)
        self.addAction(self.saveCurrent)
        self.addAction(self.loadTheme)
        self.addAction(self.previewTheme)
        self.addMenu(self.themeMenu)
        self.loadTheme.setDisabled(True)
        self.previewTheme.setDisabled(True)
        self.resetAction.triggered.connect(self.resetClicked.emit)
        self.saveCurrent.triggered.connect(self.saveCurrentClicked.emit)
        self.loadTheme.triggered.connect(self.loadTheme.emit)
        self.previewTheme.triggered.connect(self.previewTheme.emit)
        self.themeactions = []
        self.themeMenu.addSeparator()


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

    displayStyles = Signal()

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
        self.saveAction = QAction("Save")
        self.exitAction.triggered.connect(exitApp)
        self.addAction(self.exitAction)
        self.addAction(self.saveAction)
