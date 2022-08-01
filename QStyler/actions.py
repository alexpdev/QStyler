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
from pathlib import Path

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFileDialog

from QStyler.utils import QssParser

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


class LoadAction(QAction):
    """Action for loading new themes from Qss file."""

    loaded = Signal([dict, str])

    def __init__(self, *args, **kwargs):
        """Construct action."""
        super().__init__(*args, **kwargs)
        self.triggered.connect(self.loadTheme)

    def loadTheme(self):
        """Start the dialog and get the file."""
        self.dialog = ThemeLoadDialog()
        self.dialog.closing.connect(self.getThemeFile)
        self.dialog.open()

    def getThemeFile(self, title, path):
        """Open and save data in file path as title theme."""
        if path and title:
            parser = QssParser(path)
            theme = parser.result
            final = {}
            for row in theme:
                final.update(row)
            self.loaded.emit(final, title)
