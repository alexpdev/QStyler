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
"""Module for styler tab and styler table."""

import re

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFontMetrics, QValidator
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
                               QLabel, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QSplitter, QTextBrowser)

from QStyler.toolbar import ToolBar
from QStyler.utils import blockSignals
from QStyler.combos import PropsCombo, WidgetCombo, StateCombo, ControlCombo


class Table(QTableWidget):
    """Table containing all of the styles available for editing."""

    widgetChanged = Signal([str])
    setNewRow = Signal()

    def __init__(self, manager, parent=None) -> None:
        """Initialize the styler table."""
        super().__init__(parent=parent)
        self.manager = manager
        self.widget = parent
        self.setColumnCount(2)
        self.setRowCount(0)
        self.loadProps()
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        self.setHorizontalHeader(header)
        self.verticalHeader().setHidden(True)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.cellChanged.connect(self.saveProp)
        self.widgetChanged.connect(self.loadProps)

    @blockSignals
    def loadProps(self, common=None):
        """Load items into table."""
        if common is None:
            common = {}
        rowcount = self.rowCount()
        for i, key in enumerate(common):
            if i < rowcount:
                self._setRowData(i, key, common[key])
            else:
                self.addRow(key=key, value=common[key])
        if self.rowCount() == 1 and not self.item(0, 1).text():
            return
        while self.rowCount() > len(common):
            self.removeRow(self.rowCount() - 1)
        self.addRow()

    @blockSignals
    def _setRowData(self, rownum, key, value):
        """Do something."""
        self.item(rownum, 1).setText(value)
        self.cellWidget(rownum, 0).selectKey(key)

    def indexFromWidget(self, widget):
        """
        Find the row index for the given combobox.

        Parameters
        ----------
        widget : PropCombo
            properties combo box.

        Returns
        -------
        int | None
            row index
        """
        for i in range(self.rowCount()):
            current = self.cellWidget(i, 0)
            if widget is current:
                return i
        return None  # pragma: nocover

    @blockSignals
    def addRow(self, key=None, value=""):
        """Add a new row to the table."""
        cbox = PropsCombo(self.manager.data, parent=self)
        rownum = self.rowCount()
        self.insertRow(rownum)
        self.setCellWidget(rownum, 0, cbox)
        item = QTableWidgetItem(type=0)
        flag1 = Qt.ItemFlag.ItemIsEditable
        flag2 = Qt.ItemFlag.ItemIsEnabled
        flag3 = Qt.ItemFlag.ItemIsSelectable
        item.setFlags(flag1 | flag2 | flag3)
        self.setItem(rownum, 1, item)
        self._setRowData(rownum, key, value)

    def saveProp(self, row, column):
        """Save the newly changed value into the current stylesheet."""
        if column == 0:
            self.updateProp(row, column)
        else:
            prop = self.cellWidget(row, 0).currentText()
            value = self.item(row, 1).text()
            title = self.widget.getWidgetState()
            if not prop or prop == "":
                return  # pragma: nocover
            self.manager.append_sheet(title, prop, value)
        self.setNewRow.emit()

    def currentSheet(self):
        """Retreive the current stylesheet from the factory."""
        title = self.widget.getWidgetState()
        sheet = self.manager.get_sheet(title)
        return sheet

    @blockSignals
    def updateProp(self, row, column):
        """Update property when combobox value changes."""
        cbox = self.cellWidget(row, column)
        prop = cbox.currentText()
        sheet = self.currentSheet()
        if prop in sheet:
            self.item(row, 1).setText(sheet[prop])  # pragma: nocover
        else:
            self.item(row, 1).setText("")


class StylerTab(QWidget):
    """Tab containing the table that changes the styling for the widgets."""

    statusChanged = Signal([str])

    def __init__(self, parent=None):
        """Initialize the styler tab."""
        super().__init__(parent=parent)
        self.window = parent
        self.manager = parent.manager
        self.data = self.manager.data
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.widget_label = QLabel("Widget(s)")
        self.control_label = QLabel("Control")
        self.state_label = QLabel("State")
        self.combo = WidgetCombo(self.data, parent=self)
        self.control_combo = ControlCombo(self.data, parent=self)
        self.state_combo = StateCombo(self.data, parent=self)
        self.table = Table(self.manager, parent=self)
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.table)
        self.browser = QTextBrowser(self)
        self.browser.sizePolicy().setVerticalPolicy(self.sizePolicy().Maximum)
        self.browser.setMaximumHeight(120)
        self.splitter.addWidget(self.browser)
        self.vlayout1 = QVBoxLayout()
        self.vlayout2 = QVBoxLayout()
        self.vlayout3 = QVBoxLayout()
        self.vlayout1.addWidget(self.widget_label)
        self.vlayout1.addWidget(self.combo)
        self.vlayout2.addWidget(self.control_label)
        self.vlayout2.addWidget(self.control_combo)
        self.vlayout3.addWidget(self.state_label)
        self.vlayout3.addWidget(self.state_combo)
        self.mainGroup = QGroupBox(parent=self)
        self.mainGroup.setTitle("Widget Control Group")
        self.mainGroup.setFlat(False)
        self.hlayout = QHBoxLayout()
        self.mainGroup.setLayout(self.hlayout)
        self.hlayout.addLayout(self.vlayout1)
        self.hlayout.addLayout(self.vlayout2)
        self.hlayout.addLayout(self.vlayout3)
        self.layout.addWidget(self.mainGroup)
        self.layout.addWidget(self.splitter)

        self.table.setNewRow.connect(self.addTableRow)
        self.combo.widgetChanged.connect(self.statusChanged.emit)
        self.state_combo.currentIndexChanged.connect(self.statusChanged.emit)
        self.control_combo.currentIndexChanged.connect(self.statusChanged.emit)
        self.statusChanged.connect(self.updateTable)
        self.boxgroups = []

    def updateTable(self, _):
        """Update table to new status."""
        state = self.getWidgetState()
        common = self.manager.get_sheet(state)
        self.table.loadProps(common=common)

    def add_widget_combo(self):
        """Add a widget combo box group."""
        boxlen = len(self.boxgroups)
        text = self.getWidgetState()
        if len(text.split(",")) >= boxlen + 1:

            groupbox = GroupBox(parent=self)
            self.layout.insertWidget(boxlen + 2, groupbox)
            self.boxgroups.append(groupbox)
        else:
            self.window.statusbar.showMessage("Empty Widget Group Exists.",
                                              4000)

    def minus_widget_combo(self):
        """Remove a widget combo box group."""
        if len(self.boxgroups) > 0:
            groupbox = self.boxgroups[-1]
            groupbox.delete_widgets()
            index = self.layout.indexOf(groupbox)
            self.layout.takeAt(index)
            self.boxgroups = self.boxgroups[:-1]
            groupbox.deleteLater()
            groupbox.destroy()
        else:
            self.window.statusbar.showMessage("Nothing to remove.", 4000)

    def addTableRow(self):
        """Add a new row to the table."""
        for row in range(self.table.rowCount()):
            text = self.table.cellWidget(row, 0).currentText()
            if text in ["", "-"]:
                return
        self.table.addRow()

    def getWidgetState(self) -> str:
        """
        Get the current state of the combo boxes.

        Returns
        -------
        str
            the current state as a string
        """
        widgets = []
        for box in self.boxgroups + [self]:
            widget = box.combo.currentText()
            control = box.control_combo.currentText()
            state = box.state_combo.currentText()
            parts = []
            if widget:
                parts.append(widget)
            if control:
                parts += [":", control]
            if state:
                parts += ["::", state]
            full = "".join(parts)
            if full:
                widgets.append(full)
        text = ",".join(widgets)
        return text


class GroupBox(QGroupBox):
    """Custom Group Box."""

    def __init__(self, parent=None):
        """Initialize Group Box Constructor."""
        super().__init__(parent=parent)
        self.widget = parent
        self.data = parent.data
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.combo = WidgetCombo(self.data, parent=self)
        self.control_combo = ControlCombo(self.data, parent=self)
        self.state_combo = StateCombo(self.data, parent=self)
        self.layout.addWidget(self.combo)
        self.layout.addWidget(self.control_combo)
        self.layout.addWidget(self.state_combo)
        self.state_combo.currentIndexChanged.connect(parent.statusChanged.emit)
        self.control_combo.currentIndexChanged.connect(
            parent.statusChanged.emit)
        self.combo.widgetChanged.connect(parent.statusChanged.emit)

    def delete_widgets(self):
        """Delete all widgets in the GroupBox."""
        for combo in [self.combo, self.control_combo, self.state_combo]:
            index = self.layout.indexOf(combo)
            item = self.layout.takeAt(index)
            combo.deleteLater()
            item.widget().deleteLater()
