import sys
import os
import json
from typing import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class MenuBar(QMenuBar):
    """
    Create a mainwindow menu bar for the default menubar.

    Parameters
    ----------
    parent : QWidget
        This widgets parent.
    """

    def __init__(self, parent) -> None:
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
        Create the menu widget

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
        super().__init__(text, parent=parent)
        self.themes = json.load(open("QStyler/style/prestyles.json","rt"))
        self.resetAction = QAction("Reset")
        self.addAction(self.resetAction)
        self.resetAction.triggered.connect(self.resetStyleSheet)
        self.themeMenu = QMenu("Themes", parent=self)
        self.addMenu(self.themeMenu)
        self.themeactions = {}
        for key in self.themes:
            action = QAction(key)
            action.setObjectName(key+"action")
            action.triggered.connect(self.applyTheme)
            self.themeactions[action] = key
            self.themeMenu.addAction(action)

    def applyTheme(self):
        """Apply chosen theme to mainwindow and application."""
        sender = self.sender()
        theme = {}
        for k,v in self.themeactions.items():
            if k == sender:
                theme = self.themes[v]
                break
        sheet = []
        for key,val in theme.items():
            sheet.append({key:val})
        self.parent().window.tab1.table.ssfactory.sheets = sheet
        self.parent().window.tab1.table.ssfactory.update_styleSheet()

    def resetStyleSheet(self):
        """Reset the current style sheet to blank."""
        parent = self.parent()
        parent.window.tab1.table.ssfactory.sheets = []
        sheet = parent.window.tab1.table.ssfactory.update_styleSheet()
        self.parent().window.setStyleSheet(sheet)
        parent.window.tab1.setStyleSheet(sheet)
        parent.window.tab2.setStyleSheet(sheet)


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
        super().__init__(text, parent=parent)
        self.exitAction = QAction("Exit")
        self.showAction = QAction("Show StyleSheet")
        self.exitAction.triggered.connect(self.exitApp)
        self.showAction.triggered.connect(self.showStyles)
        self.addAction(self.showAction)
        self.addAction(self.exitAction)

    def exitApp(self):
        """Quit the application."""
        qapp = QApplication.instance()
        qapp.quit()

    def showStyles(self):
        """Show the current stylesheet in a separate widget."""
        sheet = self.parent().window.tab2.table.ssfactory.update_styleSheet()
        self.dialog = QWidget()
        layout = QVBoxLayout()
        self.dialog.setLayout(layout)
        textEdit = QTextBrowser(parent=self.dialog)
        textEdit.setPlainText(sheet)
        layout.addWidget(textEdit)
        self.dialog.show()
