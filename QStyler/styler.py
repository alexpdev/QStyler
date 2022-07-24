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
from PySide6.QtGui import QValidator
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QTableWidget,
                               QTableWidgetItem, QVBoxLayout, QWidget, QToolButton)

from QStyler.utils import blockSignals


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
    def loadProps(self, widget=None):
        """Load items into table."""
        sheet = self.manager.get_sheet(widget)
        rowcount = self.rowCount()
        for i, key in enumerate(sheet):
            if i < rowcount:
                self._setRowData(i, key, sheet[key])
            else:
                self.addRow(key=key, value=sheet[key])
        while self.rowCount() > len(sheet):
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
        self.resizeRowsToContents()

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
            self.manager.addSheet(title, prop, value)
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
            self.item(row, 1).setText(sheet[prop])
        else:
            self.item(row, 1).setText("")


class PropsCombo(QComboBox):
    """Combobox storing all available properties that can be edited."""

    def __init__(self, data, parent=None):
        """Initialize the properties combo box."""
        super().__init__(parent=parent)
        self.widget = parent
        self.app = QApplication.instance()
        self.info = data
        self.tableItem = None
        self.addItem("-")
        self.loadItems()
        self.currentIndexChanged.connect(self.notifyTable)
        self.setSizeAdjustPolicy(self.sizeAdjustPolicy().AdjustToContents)

    def notifyTable(self, _):
        """Update table cell with accurate information."""
        rownum = self.widget.indexFromWidget(self)
        self.widget.saveProp(rownum, 0)

    def loadItems(self):
        """Populate the combo box with values from json file."""
        for prop in self.info["properties"]:
            self.addItem(prop)

    @blockSignals
    def selectKey(self, key):
        """Select the appropriate item as current index."""
        for i in range(self.count()):
            if self.itemText(i) == key:
                self.setCurrentIndex(i)
                break


class WidgetCombo(QComboBox):
    """Combo box containing all of the available widgets."""

    widgetChanged = Signal([str])

    def __init__(self, data, parent=None):
        """Initialize widget combo box."""
        super().__init__(parent=parent)
        self.widget = parent
        self.info = data
        self.addItem("")
        self.addItem("*")
        self.loadItems()
        self.setEditable(True)
        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.setInsertPolicy(self.NoInsert)
        validator = WidgetValidator(parent=self)
        self.setValidator(validator)
        self.currentTextChanged.connect(self.widgetChanged.emit)

    def loadItems(self):
        """Populate combobox with data."""
        widgets = self.info["controls"]
        for widget in widgets:
            self.addItem(widget)


class ControlCombo(QComboBox):
    """ComboBox containing all of the widget controls."""

    def __init__(self, data, parent=None):
        """Initialize the control combo box."""
        super().__init__(parent=parent)
        self.widget = parent
        self.info = data
        self.addItem("")
        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.widget.combo.widgetChanged.connect(self.loadControls)

    @blockSignals
    def loadControls(self, widget):
        """Populate the the combobox with data from jsonfile."""
        for _ in range(self.count()):
            self.removeItem(0)
        self.addItem("")
        widgets = widget.split(" ")
        if len(widgets) > 1:
            widget = widget[-1]
        if widget in self.info["controls"]:
            for control in self.info["controls"][widget]:
                self.addItem(control)


class StateCombo(QComboBox):
    """Combobox with all the widget states available."""

    def __init__(self, data, parent=None):
        """Initialize the states combo box."""
        super().__init__(parent=parent)
        self.widget = parent
        self.info = data
        self.addItem("")
        self.loadStates()
        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)

    def loadStates(self):
        """Populate with data from jsonfile."""
        for state in self.info["states"]:
            self.addItem(state)


class StylerTab(QWidget):
    """Tab containing the table that changes the styling for the widgets."""

    def __init__(self, parent=None):
        """Initialize the styler tab."""
        super().__init__(parent=parent)
        self.manager = parent.manager
        self.data = self.manager.data
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.widget_label = QLabel("Widget(s)")
        self.control_label = QLabel("Control")
        self.state_label = QLabel("State")
        self.plusbtn = QToolButton(parent=self)
        self.plusbtn.setText("+")
        self.minusbtn = QToolButton(parent=self)
        self.minusbtn.setText("-")
        self.combo = WidgetCombo(self.data, parent=self)
        self.control_combo = ControlCombo(self.data, parent=self)
        self.state_combo = StateCombo(self.data, parent=self)
        self.button = QPushButton("Save Theme", parent=self)
        self.table = Table(self.manager, parent=self)
        self.vlayout1 = QVBoxLayout()
        self.vlayout2 = QVBoxLayout()
        self.vlayout3 = QVBoxLayout()
        self.vlayout4 = QVBoxLayout()
        self.vlayout1.addWidget(self.widget_label)
        self.vlayout1.addWidget(self.combo)
        self.vlayout2.addWidget(self.control_label)
        self.vlayout2.addWidget(self.control_combo)
        self.vlayout3.addWidget(self.state_label)
        self.vlayout3.addWidget(self.state_combo)
        self.vlayout4.addWidget(self.plusbtn)
        self.vlayout4.addWidget(self.minusbtn)
        self.hlayout = QHBoxLayout()
        self.hlayout.addLayout(self.vlayout4)
        self.hlayout.addLayout(self.vlayout1)
        self.hlayout.addLayout(self.vlayout2)
        self.hlayout.addLayout(self.vlayout3)
        self.layout.addLayout(self.hlayout)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.button)
        self.control_combo.currentTextChanged.connect(self.emitChanges)
        self.state_combo.currentTextChanged.connect(self.emitChanges)
        self.plusbtn.clicked.connect(self.add_widget_combo)
        self.table.setNewRow.connect(self.addTableRow)
        self.combogroups = []

    def add_widget_combo(self):
        layout = QHBoxLayout()
        widget_combo = WidgetCombo(self.data, parent=self)
        control_combo = ControlCombo(self.data, parent=self)
        state_combo = StateCombo(self.data, parent=self)
        layout.addWidget(widget_combo)
        layout.addWidget(control_combo)
        layout.addWidget(state_combo)
        self.layout.insertLayout(1,layout)




    def addTableRow(self):
        """
        Add a new row to the table.
        """
        for row in range(self.table.rowCount()):
            text = self.table.cellWidget(row, 0).currentText()
            if text == "-":
                return
        self.table.addRow()

    def setLineReadOnly(self, ischecked: bool):
        """
        Set the line edit as read only.

        Parameters
        ----------
        ischecked : bool
            if is checked.
        """
        self.lineedit.setReadOnly(ischecked)

    @blockSignals
    def emitChanges(self, _: str) -> None:
        """
        Send signals to table widget.

        Parameters
        ----------
        data : str
            _description_
        """
        self.lineedit.clear()
        text = self.widget_combo.currentText()
        control = self.control_combo.currentText()
        state = self.state_combo.currentText()
        result = "".join([i for i in [text, control, state] if i])
        result = "*" if not result else result
        self.lineedit.setText(result)
        self.table.widgetChanged.emit(result)

    def getWidgetState(self) -> str:
        """
        Get the current state of the combo boxes.

        Returns
        -------
        str
            the current state as a string
        """
        text = self.lineedit.text()
        return text if text else "*"


class WidgetValidator(QValidator):
    """
    Text validator for Widget Combo Box.
    """

    def __init__(self, parent=None):
        """Construct the validator."""
        super().__init__(parent=parent)
        self.widget = parent
        self.widget_list = []
        for i in range(self.widget.count()):
            text = self.widget.itemText(i)
            self.widget_list.append(text)

    def fixup(self, text):
        """Fix the text when it is invalid."""
        while self.validate(text) == self.Invalid:
            text = text[:-1]

    def validate(self,text, pos=None):
        """Authenticate whether text is valid."""
        if text == "":
            return self.Intermediate
        def test_match(text):
            """Test text to see if it is valid."""
            l = len(text)
            for widget in self.widget_list:
                if len(widget) < l:
                    continue
                if len(widget) == l:
                    if text == widget:
                        return self.Acceptable
                if len(widget) > l:
                    if text in widget:
                        return self.Intermediate
        pat1 = re.compile(r"^\w+?\s$")
        pat2 = re.compile(r"^\w+?\s\w+$")
        if pat2.match(text):
            widgets = text.split(" ")
            if widgets[0] in self.widget_list:
                result = test_match(widgets[1])
                return self.Invalid if result is None else result
            return self.Invalid
        if pat1.match(text):
            widgets = text.split(" ")
            if widgets[0] in self.widget_list:
                return self.Intermediate
            return self.Invalid
        result = test_match(text)
        return self.Invalid if result is None else result
