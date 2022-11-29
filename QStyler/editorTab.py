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
"""Widget tab module."""

from PySide6.QtWidgets import (QLabel, QPlainTextEdit, QTextBrowser, QTextEdit,
                               QVBoxLayout, QWidget)

from QStyler.utils import Lorem


class EditorsTab(QWidget):
    """Tab holding all of the widgets for example style will look like."""

    def __init__(self, parent=None):
        """Initialize the widgets tab."""
        super().__init__(parent=parent)
        lorem = Lorem()
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)
        self.textEdit = QTextEdit(self)
        self.textBrowser = QTextBrowser(self)
        self.plainTextEdit = QPlainTextEdit(self)
        self.teditlabel = QLabel("QTextEdit")
        self.tbrowserlabel = QLabel("QTextBrowser")
        self.pteditlabel = QLabel("QPlainTextEdit")
        self.vpteditlay = QVBoxLayout()
        self.vtbrowslay = QVBoxLayout()
        self.vteditlay = QVBoxLayout()
        self.vpteditlay.addWidget(self.pteditlabel)
        self.vpteditlay.addWidget(self.plainTextEdit)
        self.vteditlay.addWidget(self.teditlabel)
        self.vteditlay.addWidget(self.textEdit)
        self.vtbrowslay.addWidget(self.tbrowserlabel)
        self.vtbrowslay.addWidget(self.textBrowser)
        self.vlayout.addLayout(self.vteditlay)
        self.vlayout.addLayout(self.vtbrowslay)
        self.vlayout.addLayout(self.vpteditlay)
        self.plainTextEdit.setPlainText(lorem.gentext()[:200])
        self.textEdit.setText(lorem.gentext()[200:])
        self.textBrowser.setText(lorem.gentext())
