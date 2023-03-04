from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class RenameDialog(QDialog):
    renamed = Signal(str, str)

    def __init__(self, name=None, parent=None) -> None:
        super().__init__(parent=parent)
        self.name = name
        self.setContentsMargins(3,3,3,3)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(3,3,3,3)
        self.label = QLabel(name)
        self.setWindowTitle('Rename Theme')
        self.line = QLineEdit(self)
        self.button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save", self)
        self.cancel_btn = QPushButton("Cancel", self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line)
        self.layout.addLayout(self.button_layout)
        self.button_layout.addWidget(self.save_btn)
        self.button_layout.addWidget(self.cancel_btn)
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.close)

    def save(self):
        text = self.line.text()
        self.renamed.emit(text, self.name)
        self.close()


class NewDialog(RenameDialog):
    named = Signal(str)

    def __init__(self, name=None, parent=None):
        super().__init__(parent=parent)
        self.label.setText("Set Theme Name")
        self.setWindowTitle("New Theme")

    def save(self):
        name = self.line.text()
        self.named.emit(name)
        self.close()
