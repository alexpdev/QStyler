from typing import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class Table(QTableWidget):
    def __init__(self, rows, cols, parent=None) -> None:
        super().__init__(rows, cols, parent=parent)
        self.data = [{'QAbstractScrollArea': {'props': ['background-attachment'], 'controls': ['::corner']}}, {'QCheckBox': {'props': ['background', 'background-clip', 'background-origin', 'border', 'border-color', 'border-image', 'border-radius', 'border-style', 'border-width', 'font', 'font-family', 'icon-size', 'margin', 'max-height', 'max-width', 'min-height', 'min-width', 'padding', 'spacing*'], 'controls': ['::indicator']}}, {'QColumnView': {'props': [], 'controls': []}}, {'QComboBox': {'props': ['background', 'background-clip', 'background-origin', 'border', 'border-color', 'border-image', 'border-radius', 'border-style', 'border-width', 'margin', 'max-height', 'max-width', 'min-height', 'min-width', 'padding'], 'controls': ['::down-arrow', '::drop-down']}}, {'QDateEdit': {'props': [], 'controls': []}}, {'QDateTimeEdit': {'props': [], 'controls': []}}, {'QDialog': {'props': ['background', 'background-clip', 'background-origin'], 'controls': []}}, {'QDialogButtonBox': {'props': ['button-layout', 'dialogbuttonbox-buttons-have-icons'], 'controls': []}}, {'QDockWidget': {'props': [], 'controls': ['::close-button', '::float-button', '::title']}}, {'QDoubleSpinBox': {'props': [], 'controls': []}}, {'QFrame': {'props': ['background', 'background-image', 'background-repeat', 'background-position', 'background-clip', 'background-origin', 'border', 'border-color', 'border-image', 'border-radius', 'border-style', 'border-width', 'margin', 'max-height', 'max-width', 'min-height', 'min-width', 'padding'], 'controls': []}}, {'QGroupBox': {'props': ['background', 'background-clip', 'background-origin', 'border', 'border-color', 'border-image', 'border-radius', 'border-style', 'border-width', 'margin', 'max-height', 'max-width', 'min-height', 'min-width', 'padding', 'spacing*'], 'controls': ['::indicator', '::title']}}, {'QHeaderView': {'props': [], 'controls': ['::down-arrow', '::section', '::up-arrow']}}, {'QLabel': {'props': ['background', 'background-color', 'background-clip', 'background-origin', 'border', 'border-color', 'border-image', 'border-radius', 'border-style', 'border-width', 'margin', 'max-height', 'max-width', 'min-height', 'min-width', 'padding'], 'controls': []}}, {'QLineEdit': {'props': ['background', 'background-color', 'border', 'border-color', 'border-image', 'border-radius', 'border-style', 'border-width', 'lineedit-password-character*', 'lineedit-password-mask-delay*', 'margin', 'max-height', 'max-width', 'min-height', 'min-width', 'padding'], 'controls': []}}, {'QListView': {'props': ['icon-size', 'show-decoration-selected*'], 'controls': []}}, {'QListWidget': {'props': [], 'controls': []}}, {'QMainWindow': {'props': [], 'controls': ['::separator']}}, {'QMenu': {'props': ['background', 'border', 'border-color', 'border-image', 'border-radius', 'border-style', 'border-width', 'margin', 'max-height', 'max-width', 'min-height', 'min-width', 'padding'], 'controls': ['::indicator', '::icon', '::item', '::right-arrow', '::scroller', '::separator', '::tearoff']}}, {'QMenuBar': {'props': ['background', 'border', 'border-color', 'border-image', 'border-radius', 'border-style', 'border-width', 'margin', 'max-height', 'max-width', 'min-height', 'min-width', 'padding', 'spacing*'], 'controls': ['::item']}}, {'QMessageBox': {'props': ['button-layout', 'messagebox-text-interaction-flags*'], 'controls': []}}, {'QProgressBar': {'props': ['text-align'], 'controls': ['::chunk']}}, {'QPushButton': {'props': ['background', 'background-clip', 'background-origin', 'border', 'border-color', 'border-image', 'border-radius', 'border-style', 'border-width', 'color', 'icon', 'icon-size', 'margin', 'max-height', 'max-width', 'min-height', 'min-width', 'padding', 'text-align'], 'controls': ['::menu-indicator']}}, {'QRadioButton': {'props': ['background', 'background-clip', 'background-origin', 'border', 'border-color', 'border-image', 'border-radius', 'border-style', 'border-width', 'icon-size', 'margin', 'max-height', 'max-width', 'min-height', 'min-width', 'padding', 'spacing*'], 'controls': ['::indicator']}}, {'QScrollBar': {'props': [], 'controls': ['::add-line', '::add-page', '::down-arrow', '::down-button', '::handle', '::left-arrow', '::right-arrow', '::sub-line', '::sub-page', '::up-arrow']}}, {'QSizeGrip': {'props': ['max-height', 'max-width', 'min-height', 'min-width'], 'controls': []}}, {'QSlider': {'props': [], 'controls': ['::groove', '::handle']}}, {'QSpinBox': {'props': ['bottom', 'height', 'image', 'left', 'max-height', 'max-width', 'min-height', 'min-width', 'right', 'subcontrol-origin*', 'subcontrol-position*', 'top', 'width'], 'controls': ['::down-arrow', '::down-button', '::up-arrow', '::up-button']}}, {'QSplitter': {'props': ['background', 'background-clip', 'background-origin', 'border', 'border-color', 'border-image', 'border-radius', 'border-style', 'border-width', 'margin', 'max-height', 'max-width', 'min-height', 'min-width', 'padding'], 'controls': ['::handle']}}, {'QStatusBar': {'props': ['max-height', 'max-width', 'min-height', 'min-width'], 'controls': ['::item']}}, {'QTabBar': {'props': ['icon-size'], 'controls': ['::close-button', '::scroller', '::tab', '::tab-bar', '::tear']}}, {'QTabWidget': {'props': [], 'controls': ['::left-corner', '::pane', '::right-corner', '::tab-bar']}}, {'QTableView': {'props': ['gridline-color'], 'controls': []}}, {'QTableWidget': {'props': [], 'controls': []}}, {'QTextEdit': {'props': ['background', 'background-attachment', 'background-clip', 'background-origin', 'border', 'border-color', 'border-image', 'border-radius', 'border-style', 'border-width', 'font-size', 'font-style', 'margin', 'max-height', 'max-width', 'min-height', 'min-width', 'padding', 'selection-background-color*', 'selection-color*'], 'controls': []}}, {'QTimeEdit': {'props': [], 'controls': []}}, {'QToolBar': {'props': ['icon-size'], 'controls': []}}, {'QToolButton': {'props': ['min-height', 'min-width'], 'controls': ['::menu-arrow', '::menu-button']}}, {'QToolBox': {'props': ['icon-size'], 'controls': ['::tab']}}, {'QToolTip': {'props': ['background', 'background-clip', 'background-origin', 'border', 'border-color', 'border-image', 'border-radius', 'border-style', 'border-width', 'margin', 'max-height', 'max-width', 'min-height', 'min-width', 'opacity*', 'padding'], 'controls': []}}, {'QTreeView': {'props': ['alternate-background-color', 'icon-size', 'paint-alternating-row-colors-for-empty-area'], 'controls': ['::branch']}}, {'QTreeWidget': {'props': [], 'controls': []}}, {'QWidget': {'props': ['background', 'background-clip', 'background-origin', 'border', 'border-color'], 'controls': []}}]

    def switchWidget(self,widget):


class ComboBox(QComboBox):

    widgetChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.widgets = [
            'QAbstractScrollArea', 'QCheckBox', 'QColumnView',
            'QComboBox', 'QDateEdit', 'QDateTimeEdit', 'QDialog',
            'QDialogButtonBox', 'QDockWidget', 'QDoubleSpinBox',
            'QFrame', 'QGroupBox', 'QHeaderView', 'QLabel', 'QLineEdit',
            'QListView', 'QListWidget', 'QMainWindow', 'QMenu', 'QMenuBar',
            'QMessageBox', 'QProgressBar', 'QPushButton', 'QRadioButton',
            'QScrollBar', 'QSizeGrip', 'QSlider', 'QSpinBox', 'QSplitter',
            'QStatusBar', 'QTabBar', 'QTabWidget', 'QTableView', 'QTableWidget',
            'QTextEdit', 'QTimeEdit', 'QToolBar', 'QToolButton', 'QToolBox',
            'QToolTip', 'QTreeView', 'QTreeWidget', 'QWidget'
        ]
        self.addItems(self.widgets)
        self.currentTextChanged.connect(self.emitWidget)

    def emitWidget(self, text):
        self.widgetChanged.emit(text)



class Tab1(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.combo = ComboBox()
        self.table = Table(0,0, parent=self)
        self.table.
