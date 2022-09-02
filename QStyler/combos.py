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


class PropsCombo(QComboBox):
    """Combobox storing all available properties that can be edited."""

    def __init__(self, data, parent=None):
        """Initialize the properties combo box."""
        super().__init__(parent=parent)
        self.widget = parent
        self.app = QApplication.instance()
        self.info = data
        self.tableItem = None
        self.addItem("")
        self.loadItems()
        validator = PropsValidator(parent=self)
        self.setEditable(True)
        self.setValidator(validator)
        self.currentIndexChanged.connect(self.notifyTable)

    def notifyTable(self, _):
        """Update table cell with accurate information."""
        rownum = self.widget.indexFromWidget(self)
        self.widget.saveProp(rownum, 0)

    def loadItems(self):
        """Populate the combo box with values from json file."""
        font = self.font()
        metrics = QFontMetrics(font)
        longprop = ""
        for prop in self.info["properties"]:
            if len(prop) > len(longprop):
                longprop = prop
            self.addItem(prop)
        size = metrics.size(Qt.TextSingleLine, longprop)
        self.resize(size)

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
        validator.inputAccepted.connect(self.widgetChanged.emit)

    @blockSignals
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
            widget = widgets[-1]
        else:
            widget = widgets[0]
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
        self.loadStates("")
        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.widget.combo.widgetChanged.connect(self.loadStates)

    @blockSignals
    def loadStates(self, widget=""):
        """Populate with data from jsonfile."""
        for _ in range(self.count()):
            self.removeItem(0)
        self.addItem("")
        widgets = widget.split(" ")
        if len(widgets) > 1:
            widget = widgets[-1]
        else:
            widget = widgets[0]
        for state in self.info["states"]["*"]:
            self.addItem(state)
        if widget in self.info["states"]:
            for state in self.info["states"][widget]:
                self.addItem(state)


class WidgetValidator(QValidator):
    """
    Text validator for Widget Combo Box.
    """

    inputAccepted = Signal([str])

    def __init__(self, parent=None):
        """Construct the validator."""
        super().__init__(parent=parent)
        self.widget = parent
        self.widget_list = []
        self.pat1 = re.compile(r"^\w+?\s$")
        self.pat2 = re.compile(r"^\w+?\s\w+$")
        for i in range(self.widget.count()):
            text = self.widget.itemText(i)
            self.widget_list.append(text)

    @blockSignals
    def fixup(self, text):
        """Fix the text when it is invalid."""
        if self.pat2.match(text):
            widget = self.text.split(" ")[1]
        else:
            widget = text
        while True:
            for widget in self.widget_list:
                if widget.startswith(text):
                    return
            text = text[:-1]
            widget = widget[:-1]

    def validate(self, text, _=None):
        """Authenticate whether text is valid."""
        if text == "":
            return self.Intermediate

        def test_match(text):
            """Test text to see if it is valid."""
            for widget in self.widget_list:
                if len(widget) == len(text) and text == widget:
                    return True
                if len(widget) > len(text) and text in widget:
                    return None
            return False

        if self.pat2.match(text):
            widgets = text.split(" ")
            if widgets[0] in self.widget_list:
                result = test_match(widgets[1])
                if result is True:
                    self.inputAccepted.emit(text)
                    out = self.Acceptable
                else:
                    out = (self.Invalid
                           if result is False else self.Intermediate)
                return out
        if self.pat1.match(text):
            widgets = text.split(" ")
            if widgets[0] in self.widget_list:
                return self.Intermediate
            return self.Invalid
        result = test_match(text)
        if result is True:
            self.inputAccepted.emit(text)
            out = self.Acceptable
        else:
            out = self.Intermediate if result is None else self.Invalid
        return out


class PropsValidator(QValidator):
    """Validator for Props Combo."""

    def __init__(self, parent=None):
        """Construct the validator class."""
        super().__init__(parent=parent)
        self.widget = parent
        self.data = parent.info["properties"]

    def fixup(self, text):
        """Fix invalid text."""
        while text not in self.data:  # pragma: nocover
            text = text[:-1]

    def validate(self, text, _):
        """Validate text contents."""
        if text == "":
            return self.Acceptable  # pragma: nocover
        inter = False
        for prop in self.data:
            if len(text) == len(prop) and text == prop:
                return self.Acceptable
            if len(text) < len(prop) and text in prop:
                inter = True
        if inter:
            return self.Intermediate  # pragma: nocover
        return self.Invalid
