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
"""Module for initializing the actions."""

import os
import webbrowser
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog, QHBoxLayout,
                               QLabel, QLineEdit, QPlainTextEdit, QPushButton,
                               QTextBrowser, QVBoxLayout, QWidget)

from QStyler.utils import QssParser, get_manager


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
        self.resize(300, 100)
        self.label = QLabel("Theme Name", self)
        self.label2 = QLabel("File Location", self)
        self.setWindowTitle("Load Qss Theme")
        self.lineEdit = QLineEdit(self)
        self.lineEdit2 = QLineEdit(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.lineEdit2)
        self.btn1 = QPushButton("Select File", self)
        self.btn2 = QPushButton("OK", self)
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.btn1)
        self.hlayout.addWidget(self.btn2)
        self.layout.addLayout(self.hlayout)
        self.label.setAlignment(Qt.AlignLeft)
        self.btn1.clicked.connect(self.loadTheme)
        self.btn2.clicked.connect(self.closeDialog)

    def loadTheme(self):
        """Load new theme into database."""
        result = QFileDialog.getOpenFileName(self, "Select .qss File",
                                             str(Path().home()),
                                             "QSS(*.qss), Any(*)")
        if result and result[1]:
            path = result[0]
            self.lineEdit2.setText(path)
            name, _ = os.path.splitext(os.path.basename(self.path))
            self.lineEdit.setText(name)

    def closeDialog(self):
        """Close dialog and return file path if selected."""
        text = self.lineEdit.text()
        path = self.lineEdit2.text()
        self.closing.emit(text, path)
        self.close()
        self.deleteLater()


class LoadAction(QAction):
    """Action for loading new themes from Qss file."""

    loaded = Signal([dict, str])

    def __init__(self, *args, **kwargs):
        """Construct action."""
        super().__init__(*args, **kwargs)
        self.triggered.connect(self.loadTheme)

    def loadTheme(self):  # pragma: nocover
        """Start the dialog and get the file."""
        self.dialog = ThemeLoadDialog()
        self.dialog.closing.connect(self.getThemeFile)
        self.dialog.open()

    def getThemeFile(self, title: str, path: str):
        """Open and save data in file path as title theme."""
        if path and title:
            parser = QssParser(path)
            theme = parser.result
            self.loaded.emit(theme, title)


class EditAction(QAction):
    """Edit action object."""

    def edit_current_sheet(self):  # pragma: nocover
        """Edit the current sheet."""
        sheet = QApplication.instance().styleSheet()
        self.manager = get_manager()
        self.dialog = QWidget()
        self.dialog.resize(300, 450)
        layout = QVBoxLayout(self.dialog)
        textEdit = QPlainTextEdit(self.dialog)
        self.dialog.setWindowTitle("Edit Current StyleSheet")
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
        converter = QssParser(text)
        self.manager.reset()
        self.manager.sheets = converter.collection
        self.manager.set_sheet()
        self.closeDialog()


class ShowAction(QAction):
    """Show Action object."""

    def showStyles(self):  # pragma: nocover
        """Show the current stylesheet in a separate widget."""
        sheet = QApplication.instance().styleSheet()
        self.dialog = QWidget()
        self.dialog.resize(300, 400)
        layout = QVBoxLayout(self.dialog)
        self.dialog.setWindowTitle("Current Style Sheet Theme")
        textEdit = QTextBrowser(parent=self.dialog)
        textEdit.setPlainText(sheet)
        layout.addWidget(textEdit)
        self.dialog.show()


def saveQss():  # pragma: nocover
    """Save current style to file."""
    path = QFileDialog.getSaveFileName(None, "Save File", str(Path.home()),
                                       "QSS(*.qss), Any(*)")
    if path[0]:
        with open(path[0], "wt", encoding="utf-8") as fd:
            sheet = QApplication.instance().styleSheet()
            fd.write(sheet)
    return True


def opengithub():  # pragma: nocover
    """Open webbrowser to github repo."""
    webbrowser.open("https://github.com/alexpdev/QStyler")
