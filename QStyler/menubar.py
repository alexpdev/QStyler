import sys
import os
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
        self.editMenu = EditMenu("Edit", parent=self)
        self.helpMenu = HelpMenu("Help", parent=self)
        self.optionsMenu = OptionsMenu("Options", parent=self)
        self.addMenu(self.fileMenu)
        self.addMenu(self.editMenu)
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


class EditMenu(QMenu):
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
        super().__init__(text, parent=parent)
        self.resetAction = QAction("reset")
        self.addAction(self.resetAction)
        self.resetAction.triggered.connect(self.resetStyleSheet)

    def resetStyleSheet(self):
        """Reset the current style sheet to blank."""
        pass


class OptionsMenu(QMenu):
    """
    Creates Options menu for the mainwindow menu bar.

    Parameters
    ----------
    text : str
        The text displayed on the menubar
    parent : QWidget
        This widgets parent widget
    """

    def __init__(self, text: str, parent=None) -> None:
        super().__init__(text, parent=parent)
        self.positions = QMenu("Widget Positions")
        self.position_tab2 = QAction("Tab2")
        self.position_extend_tab1 = QAction("Tab1")
        self.position_tab2.triggered.connect(self.change_tab2)
        self.position_extend_tab1.triggered.connect(self.change_tab1)
        self.addAction(self.position_tab2)
        self.addAction(self.position_extend_tab1)

    def change_tab1(self):
        """Change position of widgets to extend tab1."""
        pass

    def change_tab2(self):
        """Change the position of widgets to second tab."""
        pass


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
        sheet = self.parent().window.tab.table.ssfactory.update_styleSheet()
        dialog = QWidget()
        layout = QVBoxLayout()
        dialog.setLayout(layout)
        textEdit = QTextBrowser()
        textEdit.setPlainText(sheet)
        dialog.show()
