
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QTreeWidget, QComboBox, QApplication, QTreeWidgetItem
from QStyler.utils import blockSignals

class WidgetCombo(QComboBox):
    """Combo box containing all of the available widgets."""

    widgetChanged = Signal([str])

    def __init__(self, data, parent=None):
        """Initialize widget combo box."""
        super().__init__(parent=parent)
        self.widget = parent
        self.info = data
        self.addItem("*")
        self.loadItems()
        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.currentTextChanged.connect(self.widgetChanged.emit)

    def loadItems(self):
        """Populate combobox with data."""
        widgets = self.info["controls"]
        for widget in widgets:
            self.addItem(widget)


class WidgetTree(QTreeWidget):
    rowAdded = Signal([int])

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.manager = parent.manager
        self.setColumnCount(2)
        policy = self.sizePolicy()
        self.setSizePolicy(policy.MinimumExpanding, policy.MinimumExpanding)
        self.setHeaderHidden(True)
        self.addRow()
        self.rowAdded.connect(self.addCol)

    def addRow(self):
        item = QTreeWidgetItem(type=0)
        widget = WidgetCombo(self.manager.data, parent=self)
        self.addTopLevelItem(item)
        self.setItemWidget(item, 0,widget)
        self.setColumnWidth(0, 200)
        self.rowAdded.emit(self.topLevelItemCount())
        widget.widgetChanged.connect(self.addRow)

    def addCol(self, number):
        item = QTreeWidgetItem(type=0)
        widget = WidgetCombo(self.manager.data, parent=self)
        top = self.topLevelItem(number)
        top.addChild(item)
        self.setItemWidget(item, number, widget)
