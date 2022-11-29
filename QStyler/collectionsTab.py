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

from PySide6.QtWidgets import (QLabel, QListWidget, QListWidgetItem,
                               QTableWidget, QTableWidgetItem, QTreeWidget,
                               QTreeWidgetItem, QVBoxLayout, QWidget)

from QStyler.utils import Lorem


class CollectionsTab(QWidget):
    """Tab holding all of the widgets for example style will look like."""

    def __init__(self, parent=None):
        """Initialize the widgets tab."""
        super().__init__(parent=parent)
        lorem = Lorem()
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)
        self.listWidget = QListWidget(self)
        self.treelabel = QLabel("QTreeWidget")
        self.tablelabel = QLabel("QTableWidget")
        self.listlabel = QLabel("QListWidget")
        for _ in range(15):
            item = QListWidgetItem(type=0)
            item.setText(" ".join([lorem.genword() for _ in range(15)]))
            self.listWidget.addItem(item)
        self.treeWidget = QTreeWidget(self)
        self.treeWidget.setColumnCount(2)
        for _ in range(15):
            root = QTreeWidgetItem(type=0)
            root.setText(0, lorem.genword())
            root.setText(1, " ".join([lorem.genword() for _ in range(12)]))
            self.treeWidget.addTopLevelItem(root)
            for _ in range(15):
                item = QTreeWidgetItem(type=0)
                item.setText(0, lorem.genword())
                item.setText(1, " ".join([lorem.genword() for _ in range(12)]))
                root.addChild(item)
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(15)
        self.tableWidget.setRowCount(0)
        for i in range(15):
            self.tableWidget.insertRow(i)
            for j in range(15):
                item1 = QTableWidgetItem(type=0)
                item1.setText(lorem.genword())
                self.tableWidget.setItem(i, j, item1)
        self.vlistlay = QVBoxLayout()
        self.vtreelay = QVBoxLayout()
        self.vtablelay = QVBoxLayout()
        self.vlistlay.addWidget(self.listlabel)
        self.vlistlay.addWidget(self.listWidget)
        self.vtreelay.addWidget(self.treelabel)
        self.vtreelay.addWidget(self.treeWidget)
        self.vtablelay.addWidget(self.tablelabel)
        self.vtablelay.addWidget(self.tableWidget)
        self.vlayout.addLayout(self.vlistlay)
        self.vlayout.addLayout(self.vtablelay)
        self.vlayout.addLayout(self.vtreelay)
