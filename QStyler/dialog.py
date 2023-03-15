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
"""Module for dialogs."""

from pathlib import Path

from PySide6.QtCore import Signal, QSize, Qt
from PySide6.QtWidgets import (QDialog, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QVBoxLayout, QTextBrowser)
from PySide6.QtGui import QPixmap

from QStyler.utils import get_icon

class RenameDialog(QDialog):
    """Dialog window for renaming theme."""

    renamed = Signal(str, str)

    def __init__(self, name: str = None, parent=None) -> None:
        """
        Construct new window and get name for theme.

        Parameters
        ----------
        name : str, optional
            old theme name, by default None
        parent : QWidget, optional
            parent widget, by default None
        """
        super().__init__(parent=parent)
        self.name = name
        self.setContentsMargins(3, 3, 3, 3)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(3, 3, 3, 3)
        self.label = QLabel(name)
        self.setWindowTitle("Rename Theme")
        self.setWindowIcon(get_icon("QStylerIcon.png"))
        self.setModal(True)
        self.line = QLineEdit(self)
        self.button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save", self)
        self.cancel_btn = QPushButton("Cancel", self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line)
        self.layout.addLayout(self.button_layout)
        self.button_layout.addWidget(self.save_btn)
        self.button_layout.addWidget(self.cancel_btn)
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.close)

    def save(self):
        """
        Save the current text from the line edit as name.
        """
        text = self.line.text()
        self.renamed.emit(text, self.name)
        self.close()


class NewDialog(RenameDialog):
    """Dialog for naming new theme."""

    named = Signal(str)

    def __init__(self, name=None, parent=None):
        """
        Construct dialog for inputing name for new theme.

        Parameters
        ----------
        name : optional
             by default None
        parent : QWidget, optional
            parent widget, by default None
        """
        super().__init__(name, parent)
        self.label.setText("Set Theme Name")
        self.setWindowIcon(get_icon("QStylerIcon.png"))
        self.setWindowTitle("New Theme")
        self.setModal(True)

    def save(self):
        """
        Save the name as the title for theme.
        """
        name = self.line.text()
        self.named.emit(name)
        self.close()


class AboutQStyler(QDialog):
    """A Informational box that describes the QStyler application."""

    def __init__(self, parent=None):
        """Construct and display the about dialog."""
        super().__init__(parent=parent)
        self.setModal(True)
        self.layout = QVBoxLayout(self)
        self.label = QLabel()
        self.setWindowIcon(get_icon("QStylerIcon.png"))
        self.setWindowTitle("About QStyler")
        base = Path(__file__).parent.parent
        image = base / "assets" / "QStylerLogo.png"
        pixmap = QPixmap(str(image)).scaled(QSize(280,80))
        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.label)
        readme = base / "README.md"
        with open(readme, "rt", encoding="utf8") as fd:
            info = fd.read().split("\n")
            info = info[16:20] + info[22:]
            info = "\n".join(info)


        self.textBrowser = QTextBrowser(parent=self)
        self.layout.addWidget(self.textBrowser)
        self.textBrowser.setMarkdown(info)
        self.okay_btn = QPushButton("Okay", self)
        self.layout.addWidget(self.okay_btn)
        self.okay_btn.clicked.connect(self.close)
        self.resize(660,760)
