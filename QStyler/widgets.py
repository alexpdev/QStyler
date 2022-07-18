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

import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QCommandLinkButton, QDial, QDockWidget,
    QDoubleSpinBox, QFontComboBox, QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QKeySequenceEdit, QLabel, QLCDNumber, QLineEdit, QListWidget,
    QListWidgetItem, QPlainTextEdit, QProgressBar, QPushButton, QRadioButton,
    QScrollBar, QSlider, QSpinBox, QTableWidget, QTableWidgetItem,
    QTextBrowser, QTextEdit, QTimeEdit, QToolButton, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

from QStyler.utils import Lorem


class WidgetsTab(QWidget):
    """Tab holding all of the widgets for example style will look like."""

    def __init__(self, parent=None):
        """Initialize the widgets tab."""
        super().__init__(parent=parent)
        lorem = Lorem()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.buttonbox = QGroupBox("Buttons", self)
        self.vlay1 = QVBoxLayout()
        self.buttonbox.setLayout(self.vlay1)
        self.pushButton = QPushButton("Push Button", self)
        self.radioButton = QRadioButton("Radio Button", self)
        self.checkBox = QCheckBox("Check Box", self)
        self.keySequenceEdit = QKeySequenceEdit(self)
        self.commandLinkButton = QCommandLinkButton("Command Link", self)
        self.toolButton = QToolButton(self)
        self.toolButton.setText("ToolButton")
        self.vlay1.addWidget(self.pushButton)
        self.vlay1.addWidget(self.radioButton)
        self.vlay1.addWidget(self.toolButton)
        self.vlay1.addWidget(self.commandLinkButton)
        self.vlay1.addWidget(self.checkBox)
        self.vlay1.addWidget(self.keySequenceEdit)
        self.linebox = QGroupBox("Spin Boxes", self)
        self.vlay2 = QVBoxLayout()
        self.linebox.setLayout(self.vlay2)
        self.lineEdit = QLineEdit(self)
        self.timeEdit = QTimeEdit(self)
        self.fontComboBox = QFontComboBox(self)
        self.comboBox = QComboBox(self)
        self.spinBox = QSpinBox(self)
        self.doubleSpinBox = QDoubleSpinBox(self)
        self.textEdit = QTextEdit(self)
        self.textBrowser = QTextBrowser(self)
        self.dial = QDial(self)
        self.plainTextEdit = QPlainTextEdit(self)
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.vlay2.addWidget(self.lineEdit)
        self.vlay2.addWidget(self.comboBox)
        self.vlay2.addWidget(self.spinBox)
        self.vlay2.addWidget(self.doubleSpinBox)
        self.vlay2.addWidget(self.fontComboBox)
        self.vlay2.addWidget(self.timeEdit)
        self.horizontalbox = QGroupBox("Horizontal")
        self.vlay3 = QVBoxLayout()
        self.horizontalbox.setLayout(self.vlay3)
        self.lcdNumber = QLCDNumber(self)
        self.verticalSlider = QSlider(self)
        self.verticalSlider.setOrientation(Qt.Vertical)
        self.verticalSlider.setMinimum(0)
        self.verticalSlider.setMaximum(100)
        self.verticalSlider.setTickInterval(1)
        self.verticalScrollBar = QScrollBar(self)
        self.verticalSlider.valueChanged.connect(self.changeLCD)
        self.line2 = QFrame(self)
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.verticalScrollBar.setOrientation(Qt.Vertical)
        self.horizontalScrollBar = QScrollBar(self)
        self.horizontalScrollBar.setOrientation(Qt.Horizontal)
        self.horizontalSlider = QSlider(self)
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.progressBar = QProgressBar(self)
        self.dockWidget = QDockWidget(self)
        self.listWidget = QListWidget(self)
        self.vlay3.addWidget(self.progressBar)
        self.vlay3.addWidget(self.horizontalSlider)
        self.vlay3.addWidget(self.horizontalScrollBar)
        self.vlay3.addWidget(self.lcdNumber)
        self.vlay3.addWidget(self.line2)
        self.verticalbox = QGroupBox("Vertical", self)
        self.hlay1 = QHBoxLayout()
        self.progressBar.setRange(0, 100)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.valueChanged.connect(self.updateProgress)
        self.teditlabel = QLabel("QTextEdit")
        self.tbrowserlabel = QLabel("QTextBrowser")
        self.pteditlabel = QLabel("QPlainTextEdit")
        self.treelabel = QLabel("QTreeWidget")
        self.tablelabel = QLabel("QTableWidget")
        self.listlabel = QLabel("QListWidget")
        self.verticalbox.setLayout(self.hlay1)
        self.hlay1.addWidget(self.verticalScrollBar)
        self.hlay1.addWidget(self.verticalSlider)
        self.hlay1.addWidget(self.line)
        self.hlay1.addWidget(self.dial)
        self.grid.addWidget(self.buttonbox, 0, 0)
        self.grid.addWidget(self.linebox, 0, 1)
        self.grid.addWidget(self.horizontalbox, 0, 3)
        self.grid.addWidget(self.verticalbox, 0, 2)
        for _ in range(15):
            item = QListWidgetItem(type=0)
            item.setText(lorem.genword())
            self.listWidget.addItem(item)
        self.treeWidget = QTreeWidget(self)
        for _ in range(5):
            root = QTreeWidgetItem(type=0)
            root.setText(0, lorem.genword())
            self.treeWidget.addTopLevelItem(root)
            for _ in range(15):
                item = QTreeWidgetItem(type=0)
                item.setText(0, lorem.genword())
                root.addChild(item)
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        for _ in range(15):
            rownum = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rownum)
            item1 = QTableWidgetItem(type=0)
            item2 = QTableWidgetItem(type=0)
            item1.setText(lorem.genword())
            item2.setText(lorem.genword())
            self.tableWidget.setItem(rownum, 0, item1)
            self.tableWidget.setItem(rownum, 1, item2)
        self.vpteditlay = QVBoxLayout()
        self.vtbrowslay = QVBoxLayout()
        self.vteditlay = QVBoxLayout()
        self.vlistlay = QVBoxLayout()
        self.vtreelay = QVBoxLayout()
        self.vtablelay = QVBoxLayout()
        self.vpteditlay.addWidget(self.pteditlabel)
        self.vpteditlay.addWidget(self.plainTextEdit)
        self.vteditlay.addWidget(self.teditlabel)
        self.vteditlay.addWidget(self.textEdit)
        self.vtbrowslay.addWidget(self.tbrowserlabel)
        self.vtbrowslay.addWidget(self.textBrowser)
        self.vlistlay.addWidget(self.listlabel)
        self.vlistlay.addWidget(self.listWidget)
        self.vtreelay.addWidget(self.treelabel)
        self.vtreelay.addWidget(self.treeWidget)
        self.vtablelay.addWidget(self.tablelabel)
        self.vtablelay.addWidget(self.tableWidget)
        self.grid.addLayout(self.vteditlay, 1, 0)
        self.grid.addLayout(self.vtbrowslay, 1, 1)
        self.grid.addLayout(self.vpteditlay, 1, 2)
        self.grid.addWidget(self.dockWidget, 1, 3, -1, -1)
        self.grid.addLayout(self.vlistlay, 2, 0)
        self.grid.addLayout(self.vtablelay, 2, 1)
        self.grid.addLayout(self.vtreelay, 2, 2)
        self.dockLay = QVBoxLayout()
        self.docked = QWidget()
        self.docked.setLayout(self.dockLay)
        self.dockWidget.setWidget(self.docked)
        self.labels = []
        for _ in range(10):
            label = QLabel(lorem.genword(), parent=self)
            self.dockLay.addWidget(label)
            self.labels.append(label)
        self.plainTextEdit.setPlainText(lorem.gentext()[:200])
        self.textEdit.setText(lorem.gentext()[200:])
        self.textBrowser.setText(lorem.gentext())
        self.pushButton.clicked.connect(
            lambda: print(os.path.abspath(__file__)))

    def changeLCD(self):
        """Change the value displayed in LCD number widget."""
        slider = self.verticalSlider
        lcd = self.lcdNumber
        value = slider.value()
        lcd.display(value)

    def updateProgress(self):
        """Update value shown by progressbar."""
        slider = self.horizontalSlider
        progress = self.progressBar
        value = slider.value()
        progress.setValue(value)
