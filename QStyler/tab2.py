import json
from typing import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


def blockSignals(func):
    def wrapper(widget, *args, **kwargs):
        widget.blockSignals(True)
        result = func(widget, *args,**kwargs)
        widget.blockSignals(False)
        return result
    return wrapper

class StyleSheetFactory:

    def __init__(self):
        self.app = QApplication.instance()
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
                    ssheet += "    " + key + ": " + val + ";\n"
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


class TableItem(QTableWidgetItem):

    def assignValue(self, text, table):
        sheet = table.ssfactory.sheet



class Table(QTableWidget):

    widgetChanged = Signal()
    setNewRow = Signal()

    def __init__(self, data, parent=None) -> None:
        super().__init__(parent=parent)
        self.data = data
        self.widget = parent
        self.app = QApplication.instance()
        self.ssfactory = StyleSheetFactory()
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
    def loadProps(self):
        sheet = self.currentSheet()
        rowcount = self.rowCount()
        numkeys = len(sheet)
        for i, key in enumerate(sheet):
            if i < rowcount:
                self._setRowData(i, key, sheet[key])
            else:
                self.addRow(key=key, val=sheet[key])
        while self.rowCount() > numkeys:
            self.removeRow(self.rowCount() - 1)
        self.addRow()

    @blockSignals
    def _setRowData(self, rownum, key, value):
        self.item(rownum, 1).setText(value)


    @blockSignals
    def addRow(self, key=None, value=""):
        cbox = PropsCombo(self.data, parent=self)
        rownum = self.rowCount()
        self.insertRow(rownum)
        self.setCellWidget(rownum, 0, cbox)
        item = QTableWidgetItem(type=0)
        item.setFlags(
            Qt.ItemFlag.ItemIsEditable |
            Qt.ItemFlag.ItemIsSelectable |
            Qt.ItemFlag.ItemIsEnabled
        )
        self.setItem(rownum, 1, item)
        self._setRowData(rownum, key, value)

    def saveProp(self, row, column):
        if column == 0:
            self.updateProp(row, column)
        else:
            prop = self.cellWidget(row, 0).currentText()
            value = self.item(row, 1).text()
            title = self.widget.getWidgetState()
            self.ssfactory.addSheet(title, prop, value)
        self.setNewRow.emit()

    def currentSheet(self):
        title = self.widget.getWidgetState()
        sheet = self.ssfactory.get_sheet(title)
        return sheet

    @blockSignals
    def updateProp(self, row, column):
        cbox = self.cellWidget(row, column)
        prop = cbox.currentText()
        sheet = self.currentSheet()
        if prop in sheet:
            self.item(row,column).setText(sheet[prop])
        else:
            self.item(row, column).setText("")

    def save_theme(self):
        print(self.app.styleSheet())
        print("done")


class PropsCombo(QComboBox):

    def __init__(self, data, parent=None):
        super().__init__(parent=parent)
        self.widget = parent
        self.app = QApplication.instance()
        self.info = data
        self.tableItem = None
        self.addItem("-")
        self.loadItems()
        self.setSizeAdjustPolicy(self.sizeAdjustPolicy().AdjustToContents)
        self.currentTextChanged.connect(self.triggerRow)

    def assign(self, item):
        self.tableItem = item

    def loadItems(self):
        for prop in self.info["properties"]:
            self.addItem(prop)

    @blockSignals
    def selectKey(self, key):
        for i in range(self.count):
            if self.itemText(i) == key:
                self.setCurrentIndex(i)
                break

    def row(self):
        for i in range(self.widget.rowCount()):
            if self.widget.cellWidget(i,0) == self:
                return i
        return None

    def triggerRow(self, text):
        self.table.

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
        widgets = self.info["controls"]
        for widget in widgets:
            self.addItem(widget)

class ControlCombo(QComboBox):

    def __init__(self,data, parent=None):
        super().__init__(parent=parent)
        self.widget = parent
        self.info = data
        self.addItem("-")
        self.widget.widget_combo.currentTextChanged.connect(self.loadControls)

    @blockSignals
    def loadControls(self, widget):
        for _ in range(self.count()):
            self.removeItem(0)
        self.addItem("-")
        widget = "*" if widget == "-" else widget
        for control in self.info["controls"][widget]:
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

class Tab2(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.data = json.load(open("./QStyler/style/data.json"))
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.widget_label = QLabel("Widget")
        self.control_label = QLabel("Control")
        self.state_label = QLabel("State")
        self.lineedit = QLineEdit(parent=self)
        self.linelabel = QLabel("Target")
        for label in [self.widget_label, self.control_label, self.state_label]:
            label.setAlignment(Qt.AlignRight)
        self.widget_combo = WidgetCombo(self.data, parent=self)
        self.control_combo = ControlCombo(self.data, parent=self)
        self.state_combo = StateCombo(self.data, parent=self)
        self.checkbox = QCheckBox("Read Only", parent=self)
        self.combos = [
            self.widget_combo,
            self.control_combo,
            self.state_combo
        ]
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.widget_label)
        self.hlayout.addWidget(self.widget_combo)
        self.hlayout.addWidget(self.control_label)
        self.hlayout.addWidget(self.control_combo)
        self.hlayout.addWidget(self.state_label)
        self.hlayout.addWidget(self.state_combo)
        self.hlayout2 = QHBoxLayout()
        self.hlayout2.addWidget(self.linelabel)
        self.hlayout2.addWidget(self.lineedit)
        self.hlayout2.addWidget(self.checkbox)
        self.button = QPushButton("Save Theme", parent=self)
        self.button.clicked.connect(self.save_theme)
        self.table = Table(self.data, parent=self)
        self.layout.addLayout(self.hlayout)
        self.layout.addLayout(self.hlayout2)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.button)
        self.widget_combo.currentTextChanged.connect(self.emitChanges)
        self.control_combo.currentTextChanged.connect(self.emitChanges)
        self.state_combo.currentTextChanged.connect(self.emitChanges)
        self.checkbox.toggled.connect(self.setLineReadOnly)
        self.table.setNewRow.connect(self.addTableRow)

    def addTableRow(self):
        for row in range(self.table.rowCount()):
            text = self.table.cellWidget(row, 0).currentText()
            if text == "-":
                return
        self.table.addRow()

    def setLineReadOnly(self, ischecked):
        self.lineedit.setReadOnly(ischecked)

    def emitChanges(self):
        self.lineedit.clear()
        text = self.widget_combo.currentText()
        control = self.control_combo.currentText()
        state = self.state_combo.currentText()
        result = "".join([i for i in [text, control, state] if i != "-"])
        result = "*" if not result else result
        self.lineedit.setText(result)
        self.table.widgetChanged.emit()

    def getWidgetState(self):
        text = self.lineedit.text()
        return text if text else "*"

    def save_theme(self):
        self.table.save_theme()
