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
        self.hlayout = QHBoxLayout()
        self.setLayout(self.hlayout)
        self.buttonbox = self.button_box()
        self.linebox = self.line_box()
        self.horizontalbox, self.verticalbox = self.hv_box()
        self.dockLay = QVBoxLayout()
        self.docked = QWidget()
        self.docked.setLayout(self.dockLay)
        self.dockWidget.setWidget(self.docked)
        self.labels = []
        for _ in range(10):
            label = QLabel(lorem.genword(), parent=self)
            self.dockLay.addWidget(label)
            self.labels.append(label)
        self.pushButton.clicked.connect(
            lambda: print(os.path.abspath(__file__)))
        self.vertlay1 = QVBoxLayout()
        self.vertlay2 = QVBoxLayout()
        self.vertlay1.addWidget(self.buttonbox)
        self.vertlay1.addWidget(self.horizontalbox)
        self.vertlay2.addWidget(self.linebox)
        self.vertlay2.addWidget(self.verticalbox)
        self.hlayout.addLayout(self.vertlay1)
        self.hlayout.addLayout(self.vertlay2)
        self.hlayout.addWidget(self.dockWidget)

    def button_box(self):
        """Build ui elements for button box."""
        buttonbox = QGroupBox("Buttons", self)
        self.vlay1 = QVBoxLayout(buttonbox)
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
        return buttonbox

    def line_box(self):
        """Build ui elements for line box."""
        linebox = QGroupBox("Spin Boxes", self)
        self.vlay2 = QVBoxLayout(linebox)
        self.lineEdit = QLineEdit(self)
        self.timeEdit = QTimeEdit(self)
        self.fontComboBox = QFontComboBox(self)
        self.comboBox = QComboBox(self)
        self.spinBox = QSpinBox(self)
        self.doubleSpinBox = QDoubleSpinBox(self)
        self.vlay2.addWidget(self.lineEdit)
        self.vlay2.addWidget(self.comboBox)
        self.vlay2.addWidget(self.spinBox)
        self.vlay2.addWidget(self.doubleSpinBox)
        self.vlay2.addWidget(self.fontComboBox)
        self.vlay2.addWidget(self.timeEdit)
        return linebox

    def hv_box(self):
        """Build ui elements for hv_box."""
        self.dial = QDial(self)
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        horizontalbox = QGroupBox("Horizontal")
        self.vlay3 = QVBoxLayout(horizontalbox)
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
        self.vlay3.addWidget(self.progressBar)
        self.vlay3.addWidget(self.horizontalSlider)
        self.vlay3.addWidget(self.horizontalScrollBar)
        self.vlay3.addWidget(self.lcdNumber)
        self.vlay3.addWidget(self.line2)
        verticalbox = QGroupBox("Vertical", self)
        self.hlay1 = QHBoxLayout(verticalbox)
        self.progressBar.setRange(0, 100)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.valueChanged.connect(self.updateProgress)
        verticalbox.setLayout(self.hlay1)
        self.hlay1.addWidget(self.verticalScrollBar)
        self.hlay1.addWidget(self.verticalSlider)
        self.hlay1.addWidget(self.line)
        self.hlay1.addWidget(self.dial)
        return verticalbox, horizontalbox

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
