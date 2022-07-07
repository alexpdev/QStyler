import json
from typing import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class StyleSheetFactory:
    def __init__(self, app):
        self.app = app
        self.sheets = []

    def addSheet(self, widget, control, states, prop, value):
        if widget == "-":
            widget = "*"
        title = widget
        if control and control != "-":
            title += control
        if states is not None and "-" not in states:
            for state in states:
                title += state
        if not self.sheets:
            sheet = {title: {prop: value}}
            self.sheets.append(sheet)
            self.update_styleSheet()
            return
        for sheet in self.sheets:
            if title in sheet:
                sheet[title][prop] = value
                break
        self.update_styleSheet()

    def update_styleSheet(self):
        ssheet = ""
        for row in self.sheets:
            for k,v in row.items():
                ssheet += k + " {\n"
                for key, val in v.items():
                    ssheet += "  " + key + ": " + val + ";\n"
                ssheet += "}\n"
        self.app.setStyleSheet(ssheet)

    def get_sheet(self, widget, control, states):
        title = widget
        if control:
            title += control
        if states:
            for state in states:
                title += state
        for sheet in self.sheets:
            if title in sheet:
                return sheet[title]
        return None


class Table(QTableWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.app = parent.app
        self.ssfactory = StyleSheetFactory(self.app)
        self.widgcombo = None
        self.statecombo = None
        self.controlcombo = None
        self.setColumnCount(2)
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        self.setHorizontalHeader(header)
        self.setRowCount(0)
        self.cellChanged.connect(self.saveSheet)

    def saveSheet(self, row, col):
        widget = self.widgcombo.currentText()
        state = [self.statecombo.currentText()]
        control = self.controlcombo.currentText()
        key = self.item(row, 0).text()
        value = self.item(row, 1)
        if value is None:
            return
        self.ssfactory.addSheet(widget, control, state, key, value.text())

    def loadSheet(self, widget):
        widget = self.widgcombo.currentText()
        state = [self.statecombo.currentText()]
        control = self.controlcombo.currentText()
        sheet = self.ssfactory.get_sheet(widget, control, state)
        self.loadProps(sheet)

    def loadProps(self, props=None):
        for prop in self.info["properties"]:
            rownum = self.rowCount()
            self.insertRow(rownum)
            item = QTableWidgetItem(type=0)
            item.setText(prop)
            self.setItem(rownum, 0, item)
            if props and prop in props:
                item2 = QTableWidgetItem(type=0)
                item2.setText(props[prop])
                self.setItem(rownum, 1, item2)

    def loadinfo(self, info, widgcombo, statecombo, controlcombo):
        self.widgcombo = widgcombo
        self.statecombo = statecombo
        self.controlcombo = controlcombo
        self.widgcombo.widgetChanged.connect(self.loadSheet)
        self.statecombo.stateChanged.connect(self.loadSheet)
        self.controlcombo.controlChanged.connect(self.loadSheet)
        self.info = info
        self.loadProps()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

class WidgetCombo(QComboBox):
    widgetChanged = Signal([str])
    def __init__(self, parent=None):
        self.widget = parent
        self.info = None
        super().__init__(parent=parent)
        self.currentTextChanged.connect(self.emitWidget)

    def emitWidget(self, text):
        self.widgetChanged.emit(text)

    def loadinfo(self, info):
        self.info = info
        self.clear()
        self.addItem("-")
        for widget in self.info["widgets"]:
            self.addItem(widget)


class StateCombo(QComboBox):

    stateChanged = Signal([str])

    def __init__(self, parent=None):
        self.widget = parent
        self.info = None
        super().__init__(parent=parent)
        self.widget.widget_combo.widgetChanged.connect(self.change)
        self.currentTextChanged.connect(self.emitState)

    def loadinfo(self, info):
        self.info = info
        self.clear()
        self.addItem("-")
        for item in self.info["states"]:
            self.addItem(item)

    def change(self, text):
        self.clear()
        self.addItem("-")
        if text == "-":
            return
        widget_controls = self.info["widgets"][text]
        for control in widget_controls["controls"]:
            if control in self.info["states"]:
                self.addItem(control)

    def emitState(self, text):
        self.stateChanged.emit(text)

class ControlCombo(QComboBox):

    controlChanged = Signal([str])

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.widget = parent
        self.info = None
        self.widget.widget_combo.widgetChanged.connect(self.change)
        self.currentTextChanged.connect(self.emitControl)

    def change(self, text):
        self.clear()
        self.addItem("-")
        if text == "-":
            return
        widgetinfo = self.info["widgets"][text]
        for control in widgetinfo["controls"]:
            if "::" in control:
                self.addItem(control)

    def loadinfo(self, info):
        self.info = info
        self.clear()
        self.addItem("-")

    def emitControl(self, text):
        self.controlChanged.emit(text)

class Tab1(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.app = parent.app
        self.data = json.load(open("./QStyler/data.json"))
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.widget_label = QLabel("Widget")
        self.control_label = QLabel("Control")
        self.state_label = QLabel("State")
        self.widget_combo = WidgetCombo(parent=self)
        self.control_combo = ControlCombo(parent=self)
        self.state_combo = StateCombo(parent=self)
        self.combos = [self.widget_combo, self.control_combo,
                       self.state_combo]
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.widget_label)
        self.hlayout.addWidget(self.widget_combo)
        self.hlayout.addWidget(self.control_label)
        self.hlayout.addWidget(self.control_combo)
        self.hlayout.addWidget(self.state_label)
        self.hlayout.addWidget(self.state_combo)
        self.table = Table(parent=self)
        self.layout.addLayout(self.hlayout)
        self.layout.addWidget(self.table)
        self.fill_data()

    def fill_data(self):
        for combo in self.combos:
            combo.loadinfo(self.data)
        self.table.loadinfo(self.data, self.widget_combo, self.state_combo, self.control_combo)


# box_model = [
#  'padding-left',
#  'padding-right',
#  'padding-top',
#  'padding-bottom',
#  'margin-left',
#  'margin-right',
#  'margin-top',
#  'margin-bottom',
#  'border-left',
#  'border-right',
#  'border-top',
#  'border-bottom',
#  'background-color',
#  'color',
#  'border-width',
#  'border-style',
#  'border-radius',
#  'border-color',
#  'max-height',
#  'max-width',
#  'min-width',
#  'min-height']
