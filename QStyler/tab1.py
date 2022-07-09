import json
from typing import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


def blockSignals(func):
    def wrapper(widget, *args, **kwargs):
        widget.blockSignals(True)
        result = func(widget,*args,**kwargs)
        widget.blockSignals(False)
        return result
    return wrapper

class StyleSheetFactory:
    def __init__(self):
        self.app = qApp
        self.sheets = []

    def addSheet(self, widget, prop, value):
        for sheet in self.sheets:
            if widget in sheet:
                sheet[widget][prop] = value
                break
        else:
            self.sheets.append({widget:{prop:value}})
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
        return ssheet

    def get_sheet(self, widget):
        for sheet in self.sheets:
            if widget in sheet:
                return sheet[widget]
        return {}

    def saveToFile(self, path):
        stylesheet = self.update_styleSheet()
        with open(path, "wt") as fd:
            fd.write(stylesheet)

class Table(QTableWidget):

    widgetChanged = Signal()

    def __init__(self, data, parent=None) -> None:
        super().__init__(parent=parent)
        self.data = data
        self.widget = parent
        self.ssfactory = StyleSheetFactory()
        self.setColumnCount(2)
        self.setRowCount(0)
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        self.setHorizontalHeader(header)
        self.verticalHeader().setHidden(True)
        self.loadProps()
        self.cellChanged.connect(self.saveProp)
        self.widgetChanged.connect(self.getSheet)

    def clearAll(self):
        for _ in range(self.rowCount()):
            self.removeRow(0)
        self.clear()

    @blockSignals
    def loadProps(self, sheet={}):
        rows = self.rowCount()
        if rows == 0:
            return self.populate()
        props = self.data["properties"]
        temp = []
        for rownum in range(rows):
            key = self.item(rownum,0).text()
            value = self.item(rownum,1).text()
            temp.append(key)
            if key in sheet:
                self.item(rownum,1).setText(sheet[key])
            elif value != "":
                self.item(rownum, 1).setText("")
        if len(temp) != len(props):
            left = [i for i in props if i not in temp]
            for prop in left:
                self.addRowData(prop, "")

    def populate(self):
        for prop in self.data["properties"]:
            self.addRowData(prop, "")
        self.resizeRowsToContents()
        self.resizeColumnToContents(0)

    def addRowData(self, txt1, txt2):
        item1 = QTableWidgetItem(type=0)
        item1.setFlags(
            Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        )
        item1.setText(txt1)
        item2 = QTableWidgetItem(type=0)
        item2.setFlags(
            Qt.ItemFlag.ItemIsEditable |
            Qt.ItemFlag.ItemIsSelectable |
            Qt.ItemFlag.ItemIsEnabled
        )
        item2.setText(txt2)
        rownum = self.rowCount()
        self.insertRow(rownum)
        self.setItem(rownum, 0, item1)
        self.setItem(rownum, 1, item2)

    def getSheet(self):
        widget = self.widget.getWidgetState()
        sheet = self.ssfactory.get_sheet(widget)
        self.loadProps(sheet=sheet)

    def saveProp(self, row, column):
        value = self.item(row, column).text()
        if not value: return None
        prop = self.item(row, 0).text()
        widget = self.widget.getWidgetState()
        self.ssfactory.addSheet(widget, prop, value)

    def save_theme(self):
        print(self.app.styleSheet())

class WidgetCombo(QComboBox):

    widgetChanged = Signal([str])

    def __init__(self, data, parent=None):
        super().__init__(parent=parent)
        self.widget = parent
        self.info = data
        self.addItem("-")
        self.loadItems()
        self.currentTextChanged.connect(self.widgetChanged.emit)

    def loadItems(self):
        widgets = self.info["widgets"]
        for widget in widgets:
            self.addItem(widget)

class ControlCombo(QComboBox):

    def __init__(self,data, parent=None):
        super().__init__(parent=parent)
        self.widget = parent
        self.info = data
        self.addItem("-")
        self.widget.widget_combo.currentTextChanged.connect(self.loadControls)

    def loadControls(self, widget):
        for i in range(self.count()):
            self.removeItem(0)
        self.addItem("-")
        if "controls" in self.info["widgets"][widget]:
            for control in self.info["widgets"][widget]["controls"]:
                self.addItem(control)

class StateCombo(QComboBox):

    def __init__(self, data, parent=None):
        super().__init__(parent=parent)
        self.widget = parent
        self.info = data
        self.addItem("-")
        self.loadStates()

    def loadStates(self):
        for state in self.info["states"]:
            self.addItem(state)

class Tab1(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.data = json.load(open("./QStyler/data.json"))
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.widget_label = QLabel("Widget")
        self.control_label = QLabel("Control")
        self.state_label = QLabel("State")
        for label in [self.widget_label, self.control_label, self.state_label]:
            label.setAlignment(Qt.AlignRight)
        self.widget_combo = WidgetCombo(self.data, parent=self)
        self.control_combo = ControlCombo(self.data, parent=self)
        self.state_combo = StateCombo(self.data, parent=self)
        self.combos = [self.widget_combo, self.control_combo,
                       self.state_combo]
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.widget_label)
        self.hlayout.addWidget(self.widget_combo)
        self.hlayout.addWidget(self.control_label)
        self.hlayout.addWidget(self.control_combo)
        self.hlayout.addWidget(self.state_label)
        self.hlayout.addWidget(self.state_combo)
        self.button = QPushButton("Save Theme", parent=self)
        self.button.clicked.connect(self.save_theme)
        self.table = Table(self.data, parent=self)
        self.layout.addLayout(self.hlayout)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.button)
        self.widget_combo.currentTextChanged.connect(self.emitChanges)
        self.control_combo.currentTextChanged.connect(self.emitChanges)
        self.state_combo.currentTextChanged.connect(self.emitChanges)

    def emitChanges(self):
        self.table.widgetChanged.emit()

    def getWidgetState(self):
        widget = self.widget_combo.currentText()
        control = self.control_combo.currentText()
        state = self.state_combo.currentText()
        full = "".join([i for i in [widget, control, state] if i != "-"])
        return full if full else "*"

    def save_theme(self):
        self.table.save_theme()
