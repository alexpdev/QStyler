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

import json
import os
import re
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QFontMetricsF
from PySide6.QtWidgets import (QApplication, QComboBox, QFileDialog,
                               QHBoxLayout, QLabel, QListWidget,
                               QListWidgetItem, QSlider, QTextEdit, QToolBar,
                               QVBoxLayout, QWidget)

from QStyler.dialog import NewDialog, RenameDialog
from QStyler.utils import (ParsingError, QssParser, apply_stylesheet, get_icon,
                           json_to_stylesheet, open_github_browser)

THEMES = Path(__file__).parent / "themes"


class ColorPicker(QWidget):
    """Color picker widget."""

    colorChanged = Signal(str)

    def __init__(self, parent=None):
        """
        Construct widget for choosing colors.

        Parameters
        ----------
        parent : QWidget, optional
            parent widget, by default None
        """
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        self.label = QLabel("")
        self.red_layout = QHBoxLayout()
        self.green_layout = QHBoxLayout()
        self.blue_layout = QHBoxLayout()
        self.red_label = QLabel("R")
        self.green_label = QLabel("G")
        self.blue_label = QLabel("B")
        self.red_slider = QSlider(Qt.Horizontal)
        self.blue_slider = QSlider(Qt.Horizontal)
        self.green_slider = QSlider(Qt.Horizontal)
        self.label.setMinimumWidth(100)
        self.label.setStyleSheet("background-color: #000;")
        self.label.setMinimumHeight(150)
        self.label.setObjectName("ColorPicker")
        self.red_layout.addWidget(self.red_label)
        self.red_layout.addWidget(self.red_slider)
        self.green_layout.addWidget(self.green_label)
        self.green_layout.addWidget(self.green_slider)
        self.blue_layout.addWidget(self.blue_label)
        self.blue_layout.addWidget(self.blue_slider)
        self.layout.addWidget(self.label)
        self.layout.addLayout(self.red_layout)
        self.layout.addLayout(self.green_layout)
        self.layout.addLayout(self.blue_layout)
        self.blue_slider.setRange(0, 255)
        self.green_slider.setRange(0, 255)
        self.red_slider.setRange(0, 255)
        self.blue_slider.valueChanged.connect(self.change_color)
        self.red_slider.valueChanged.connect(self.change_color)
        self.green_slider.valueChanged.connect(self.change_color)

    def change_color(self, _):
        """
        Change color in editor.

        Parameters
        ----------
        _ : None
            unknown
        """
        blue_value = self.blue_slider.value()
        green_value = self.green_slider.value()
        red_value = self.red_slider.value()
        color_val = [f"{i:02x}" for i in [red_value, green_value, blue_value]]
        color_string = "#" + "".join(color_val)
        self.label.setStyleSheet(f"background-color: {color_string};")
        self.colorChanged.emit(color_string)


class Editor(QTextEdit):
    """Text editor widget."""


class ControlsList(QListWidget):
    """List widget for controls."""

    def __init__(self, data):
        """Construct list widget for controls."""
        super().__init__()
        self.data = data
        self.controls = set()
        for _, v in self.data["controls"].items():
            for control in v:
                self.controls.add(control)
        for control in sorted(list(self.controls)):
            item = QListWidgetItem()
            item.setText(control)
            self.addItem(item)
        self.setResizeMode(self.ResizeMode.Adjust)


class StateList(QListWidget):
    """List widget for states."""

    def __init__(self, data):
        """Construct list widget for state."""
        super().__init__()
        self.data = data
        self.states = set()
        for _, v in self.data["states"].items():
            for state in v:
                self.states.add(state)
        for state in sorted(list(self.states)):
            item = QListWidgetItem()
            item.setText(state)
            self.addItem(item)


class WidgetList(QListWidget):
    """List widget for widgets."""

    def __init__(self, data):
        """Construct list widget for widgets."""
        super().__init__()
        self.data = data
        self.widgets = set()
        for k in self.data["controls"]:
            self.widgets.add(k)
        for k in self.data["states"]:
            self.widgets.add(k)
        for widget in sorted(list(self.widgets)):
            item = QListWidgetItem()
            item.setText(widget)
            self.addItem(item)


class PropertyList(QListWidget):
    """List widget for properties."""

    def __init__(self, data):
        """Construct list widget for properties."""
        super().__init__()
        self.data = data
        self.properties = set()
        for k in self.data["properties"]:
            self.properties.add(k)
        for prop in sorted(list(self.properties)):
            item = QListWidgetItem()
            item.setText(prop)
            self.addItem(item)


class ToolBar(QToolBar):
    """Tool bar widget for themes."""

    imported = Signal(str)
    extend = Signal(bool)
    themes_dir = Path(__file__).parent / "themes"

    def __init__(self):
        """Construct tool bar."""
        super().__init__()
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.extended_state = False
        self.live_action = QAction(get_icon("live"), "live view", self)
        self.preview_action = QAction(get_icon("preview"), "preview", self)
        self.load_action = QAction(get_icon("confirm"), "load", self)
        self.reset_action = QAction(get_icon("reset"), "reset", self)
        self.load_action.setDisabled(True)
        self.live_action.setCheckable(True)
        self.live_action.setChecked(True)
        self.preview_action.setCheckable(True)
        self.preview_action.setChecked(False)
        self.preview_action.setEnabled(False)
        self.addActions(
            [
                self.live_action,
                self.load_action,
                self.preview_action,
                self.reset_action,
            ]
        )
        self.addSeparator()
        self.themes_combo = QComboBox()
        font = self.themes_combo.font()
        font.setPointSize(10)
        self.themes_combo.setFont(font)
        for file in os.listdir(self.themes_dir):
            theme_name = os.path.splitext(file)[0]
            self.themes_combo.addItem(theme_name, theme_name)
        self.addWidget(self.themes_combo)
        self.new_action = QAction(get_icon("add"), "new", self)
        self.save_action = QAction(get_icon("save"), "save", self)
        self.rename_action = QAction(get_icon("rename"), "rename", self)
        self.export_action = QAction(get_icon("export"), "export", self)
        self.import_action = QAction(get_icon("import"), "import", self)
        self.delete_action = QAction(get_icon("trash"), "delete", self)
        self.github_action = QAction(get_icon("github"), "github", self)
        self.addActions(
            [
                self.new_action,
                self.save_action,
                self.rename_action,
                self.export_action,
                self.import_action,
                self.delete_action,
            ]
        )
        self.addSeparator()
        self.addAction(self.github_action)
        self.addSeparator()
        self.extend_action = QAction(get_icon("extend-right"), "extend", self)
        self.addAction(self.extend_action)
        self.github_action.triggered.connect(open_github_browser)
        self.live_action.triggered.connect(self.activate_load)
        self.rename_action.triggered.connect(self.rename_theme)
        self.new_action.triggered.connect(self.new_dialog)
        self.delete_action.triggered.connect(self.delete_theme)
        self.import_action.triggered.connect(self.import_theme)
        self.extend_action.triggered.connect(self.on_extended)

    def on_extended(self):
        """Triggers extending the screen to view widgets while styling them."""
        if not self.extended_state:
            self.extend_action.setIcon(get_icon("extend-left"))
            self.extended_state = True
            self.extend.emit(True)
        else:
            self.extend_action.setIcon(get_icon("extend-right"))
            self.extended_state = False
            self.extend.emit(False)

    def delete_theme(self):
        """Delete the current theme in combo box."""
        theme = self.themes_combo.currentText()
        os.remove(self.themes_dir / (theme + ".json"))
        index = self.themes_combo.currentIndex()
        self.themes_combo.removeItem(index)

    def activate_load(self, state):
        """Activate or deactivate load button."""
        if state:
            self.load_action.setDisabled(True)
            self.preview_action.setDisabled(True)
        else:
            self.load_action.setDisabled(False)
            self.preview_action.setDisabled(False)

    def set_theme_name(self, new, old):
        """Set the new name for current theme."""
        for i in range(self.themes_combo.count()):
            if self.themes_combo.itemText(i) == old:
                self.themes_combo.setItemText(i, new)
                old_path = os.path.join(self.themes_dir, old + ".json")
                new_path = os.path.join(self.themes_dir, new + ".json")
                os.rename(old_path, new_path)
                break

    def rename_theme(self):
        """Rename the current theme."""
        name = self.themes_combo.currentText()
        self.dialog = RenameDialog(name, self)
        self.dialog.renamed.connect(self.set_theme_name)
        self.dialog.open()

    def set_new_name(self, name):
        """Set new theme and give it a name."""
        self.themes_combo.addItem(name)
        json.dump(
            {}, open(self.themes_dir / (name + ".json"), "wt", encoding="utf8")
        )

    def new_dialog(self):
        """Open dialog to set new theme and name."""
        self.dialog = NewDialog(None, self)
        self.dialog.named.connect(self.set_new_name)
        self.dialog.open()

    def import_theme(self):  # pragma: nocover
        """Import external qss theme into list of themes."""
        path = QFileDialog.getOpenFileName(
            parent=self, caption="Import Qss File"
        )
        if path and path[0]:
            path = path[0]
            name = os.path.split(path)[1]
            root = os.path.splitext(name)[0]
            self.themes_combo.addItem(root)
            parser = QssParser(open(path, encoding="utf8").read())
            file_path = self.themes_dir / (root + ".json")
            json.dump(
                parser.results,
                open(file_path, "wt", encoding="utf8"),
                indent=4,
            )


class StylerTab(QWidget):
    """Styler Widget."""

    extend = Signal(bool)

    def __init__(self, parent=None):
        """Construct styler widget."""
        super().__init__(parent)
        self.data = json.load(
            open(Path(__file__).parent / "data" / "data.json", encoding="utf8")
        )
        self.layout = QVBoxLayout(self)
        self.toolbar_layout = QHBoxLayout()
        self.toolbar = ToolBar()
        self.hlayout = QHBoxLayout()
        self.state_list = StateList(self.data)
        self.widget_list = WidgetList(self.data)
        self.control_list = ControlsList(self.data)
        self.property_list = PropertyList(self.data)
        self.widget_list_label = QLabel("Widgets")
        self.control_list_label = QLabel("Widget Controls")
        self.states_list_label = QLabel("Widget Pseudo-States")
        self.property_list_label = QLabel("Widget Properties")
        self.editor = Editor()
        self.vlayout = QVBoxLayout()
        self.vlayout2 = QVBoxLayout()
        self.colorPicker = ColorPicker()

        self.toolbar_layout.addStretch(1)
        self.toolbar_layout.addWidget(self.toolbar)
        self.toolbar_layout.addStretch(1)
        self.layout.addLayout(self.toolbar_layout)
        self.layout.addLayout(self.hlayout)

        self.vlayout.addWidget(self.widget_list_label)
        self.vlayout.addWidget(self.widget_list)
        self.vlayout.addWidget(self.control_list_label)
        self.vlayout.addWidget(self.control_list)
        self.vlayout.addWidget(self.states_list_label)
        self.vlayout.addWidget(self.state_list)

        self.vlayout2.addWidget(self.colorPicker)
        self.vlayout2.addWidget(self.property_list_label)
        self.vlayout2.addWidget(self.property_list)

        self.hlayout.addLayout(self.vlayout)
        self.hlayout.addWidget(self.editor)
        self.hlayout.addLayout(self.vlayout2)
        self.hlayout.setStretch(0, 1)
        self.hlayout.setStretch(1, 2)
        self.hlayout.setStretch(2, 1)
        self.editor.setTabStopDistance(
            QFontMetricsF(self.editor.font()).horizontalAdvance(" ") * 4
        )
        self.editor.setUndoRedoEnabled(True)
        self.editor.textChanged.connect(self.live_update)
        self.colorPicker.colorChanged.connect(self.insert_color)
        self.toolbar.load_action.triggered.connect(self.parse_changes)
        self.toolbar.preview_action.toggled.connect(self.preview_style)
        self.toolbar.reset_action.triggered.connect(self.reset_editor)
        self.current_style = None
        self.widget_list.itemClicked.connect(self.on_widget_clicked)
        self.widget_list.itemDoubleClicked.connect(
            self.on_widget_double_clicked
        )
        self.toolbar.save_action.triggered.connect(self.save_sheet)
        self.toolbar.themes_combo.currentTextChanged.connect(
            self.set_current_theme
        )
        self.toolbar.extend.connect(self.extend.emit)

    def save_sheet(self):
        """Save the current content of the editor to theme doc."""
        content = self.editor.toPlainText()
        parser = QssParser(content)
        results = parser.results
        name = self.toolbar.themes_combo.currentText()
        json.dump(
            results,
            open(str(THEMES / name) + ".json", "wt", encoding="utf8"),
            indent=4,
        )

    def on_widget_clicked(self, item):
        """Trigger action when button is clicked."""
        widget = item.text()
        content = self.editor.toPlainText()
        pos = self.editor.textCursor().position()
        last, moved = None, False
        if content and widget != "*":
            for match in re.finditer(widget, content):
                last = match
                if match.end() > pos:
                    cursor = self.editor.textCursor()
                    cursor.setPosition(match.end())
                    self.editor.setTextCursor(cursor)
                    self.editor.ensureCursorVisible()
                    moved = True
                    break
            if not moved and last is not None:
                cursor = self.editor.textCursor()
                cursor.setPosition(last.end())
                self.editor.setTextCursor(cursor)
                moved = True
        for row in range(self.control_list.count()):
            controls = self.data["controls"]
            item = self.control_list.item(row)
            if widget not in controls or item.text() in controls[widget]:
                item.setHidden(False)
            else:
                item.setHidden(True)
        states = self.data["states"]["*"]
        if widget in self.data["states"]:
            states += self.data["states"][widget]
        for row in range(self.state_list.count()):
            item = self.state_list.item(row)
            if item.text() not in states:
                item.setHidden(True)
            else:
                item.setHidden(False)

    def on_widget_double_clicked(self, item):
        """Trigger action when button is double clicked."""
        widget = item.text()
        content = self.editor.toPlainText()
        pos = self.editor.textCursor().position()
        for match in re.finditer(r"\}", content[pos:]):
            self.editor.textCursor().setPosition(match.end() + 1)
            self.editor.insertPlainText(f"\n{widget} {{\n\n}}")
            break
        else:
            self.editor.insertPlainText(f"\n{widget} {{\n\n}}")

    def reset_editor(self):
        """Clear the editor and current theme."""
        self.editor.clear()
        self.parse_changes()

    def set_current_theme(self, title):
        """Set the current theme to editor contents."""
        style = ""
        for path in self.toolbar.themes_dir.iterdir():
            if path.stem == title:
                data = json.load(open(path, encoding="utf8"))
                style = json_to_stylesheet(data)
        self.editor.setPlainText(style)
        self.parse_changes()

    def preview_style(self, checked):
        """Save current theme then preview contents of editor."""
        if checked:
            self.current_style = QApplication.instance().styleSheet()
            self.parse_changes()
        else:
            QApplication.instance().setStyleSheet(self.current_style)
            self.current_style = None

    def insert_color(self, color):
        """Insert color string into editor at current cursor position."""
        pattern = re.compile(r"#[a-zA-Z0-9]{3,6}\s?;?")
        pattern2 = re.compile(r"\s?rgb\(\d+,\s?\d+,\s?\d+\);?")
        cursor = self.editor.textCursor()
        pos = cursor.position()
        text = self.editor.toPlainText()
        first = max(pos - 8, 0)
        second = max(pos - 20, 0)
        result1 = pattern.search(text[first:pos])
        result2 = pattern2.search(text[second:pos])
        if result1:
            s, e = first + result1.start(), pos
            cursor.movePosition(
                cursor.MoveOperation.Left, cursor.MoveMode.KeepAnchor, e - s
            )
            cursor.deleteChar()
        elif result2:  # pragma: nocover
            s, e = second + result2.start(), pos
            cursor.movePosition(
                cursor.MoveOperation.Left, cursor.MoveMode.KeepAnchor, e - s
            )
            cursor.deleteChar()
        self.editor.insertPlainText(color + ";")

    def live_update(self):
        """Update theme in real time."""
        if self.toolbar.live_action.isChecked():
            self.parse_changes()

    def parse_changes(self):
        """Parse changes in current editor contents."""
        text = self.editor.toPlainText()
        try:
            apply_stylesheet(text)
        except ParsingError as err:  # pragma: nocover
            a = str(err)
            self.window().statusBar().showMessage(f"Error near line {a}", 2000)

    def export_theme(self):  # pragma: nocover
        """Export current editor contents to qss file."""
        current_theme = self.editor.text()
        path = QFileDialog.getSaveFileName(self, caption="Save Path")
        if path and not os.path.exists(path):
            if not path.lower().endswith(".qss"):
                path += ".qss"
            with open(path, "wt", encoding="utf8") as fd:
                fd.write(current_theme)
        else:
            self.window().statusBar().showMessage(f"Error saving to {path}")
