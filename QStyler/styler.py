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
import json
import os
from pathlib import Path
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout,
                               QLabel, QVBoxLayout, QWidget, QTextEdit, QToolBar, QListWidget, QSlider, QListWidgetItem)
from QStyler.utils import QssParser, json_to_stylesheet


class ColorPicker(QWidget):

    colorChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        self.label = QLabel("")
        self.label.setObjectName("ColorPicker")
        self.label.setMinimumHeight(150)
        self.label.setMinimumWidth(100)
        self.red_layout = QHBoxLayout()
        self.green_layout = QHBoxLayout()
        self.blue_layout = QHBoxLayout()
        self.red_label = QLabel("R")
        self.green_label = QLabel("G")
        self.blue_label = QLabel("B")
        self.red_slider = QSlider(Qt.Horizontal)
        self.blue_slider = QSlider(Qt.Horizontal)
        self.green_slider = QSlider(Qt.Horizontal)
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
        self.label.setStyleSheet("background-color: #000;")

    def change_color(self, _):
        blue_value = self.blue_slider.value()
        green_value = self.green_slider.value()
        red_value = self.red_slider.value()
        color_val = [f"{i:02x}" for i in [red_value, green_value, blue_value]]
        color_string = "#" + ''.join(color_val)
        self.label.setStyleSheet(f"background-color: {color_string};")
        self.colorChanged.emit(color_string)

class Editor(QTextEdit):

    def __init__(self):
        super().__init__()
        self.textChanged.connect

class ControlsList(QListWidget):

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.controls = set()
        for k,v in self.data["controls"].items():
            for control in v:
                self.controls.add(control)
        for control in sorted(list(self.controls)):
            item = QListWidgetItem()
            item.setText(control)
            self.addItem(item)
        self.setResizeMode(self.ResizeMode.Adjust)

class StateList(QListWidget):

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.states = set()
        for k,v in self.data["states"].items():
            for state in v:
                self.states.add(state)
        for state in sorted(list(self.states)):
            item = QListWidgetItem()
            item.setText(state)
            self.addItem(item)

class WidgetList(QListWidget):

    def __init__(self, data):
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

    def __init__(self, data):
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
    themes_dir = Path(__file__).parent / "themes"
    def __init__(self):
        super().__init__()

        self.live_action = QAction("Live View", self)
        self.live_action.setCheckable(True)
        self.live_action.setChecked(True)
        self.preview_action = QAction("preview", self)
        self.preview_action.setCheckable(True)
        self.preview_action.setChecked(False)
        self.load_action = QAction("load", self)
        self.reset_action = QAction("reset", self)
        self.addActions([self.live_action, self.load_action,
                         self.preview_action, self.reset_action])
        self.addSeparator()
        self.themes_combo = QComboBox()
        for file in os.listdir(self.themes_dir):
            theme_name = os.path.splitext(file)[0]
            self.themes_combo.addItem(theme_name, theme_name)
        self.addWidget(self.themes_combo)
        self.new_action = QAction("new", self)
        self.save_action = QAction("save", self)
        self.rename_action = QAction("rename", self)
        self.export_action = QAction("export", self)
        self.import_action = QAction("import", self)
        self.delete_action = QAction("delete", self)
        self.addActions([self.new_action, self.save_action, self.rename_action, self.export_action, self.import_action, self.delete_action])
        self.addSeparator()
        self.github_action = QAction("github", self)
        self.addAction(self.github_action)

class StylerTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = json.load(open(Path(__file__).parent / "data" / "data.json"))
        self.layout              = QVBoxLayout(self)
        self.toolbar_layout      = QHBoxLayout()
        self.toolbar             = ToolBar()
        self.hlayout             = QHBoxLayout()
        self.state_list          = StateList(self.data)
        self.widget_list         = WidgetList(self.data)
        self.control_list        = ControlsList(self.data)
        self.property_list       = PropertyList(self.data)
        self.widget_list_label   = QLabel("Widgets")
        self.control_list_label  = QLabel("Widget Controls")
        self.states_list_label   = QLabel("Widget Pseudo-States")
        self.property_list_label = QLabel("Widget Properties")
        self.editor              = Editor()
        self.vlayout             = QVBoxLayout()
        self.vlayout2            = QVBoxLayout()
        self.colorPicker         = ColorPicker()
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
        self.hlayout.setStretch(0,1)
        self.hlayout.setStretch(1,2)
        self.hlayout.setStretch(2,1)
        self.editor.textChanged.connect(self.live_update)
        self.colorPicker.colorChanged.connect(self.insert_color)
        self.toolbar.load_action.triggered.connect(self.parse_changes)
        self.toolbar.preview_action.toggled.connect(self.preview_style)
        self.toolbar.reset_action.triggered.connect(self.reset_editor)
        self.toolbar.themes_combo.currentTextChanged.connect(self.set_current_theme)
        self.current_style = None
        self.widget_list.itemClicked.connect(self.on_widget_clicked)
        self.widget_list.itemDoubleClicked.connect(self.on_widget_double_clicked)

    def on_widget_clicked(self, item):
        widget = item.text()
        content = self.editor.toPlainText()
        pos = self.editor.textCursor().position()
        last, moved = None, False
        if content and widget != "*":
            for match in re.finditer(widget, content):
                if match.end() > pos:
                    self.editor.textCursor().setPosition(match.end())
                    moved = True
                    break
                last = match
            if not moved and last is not None:
                self.editor.textCursor().setPosition(last.end())
        for row in range(self.control_list.count()):
            item = self.control_list.item(row)
            if (widget not in self.data["controls"]
            or item.text() in self.data["controls"][widget]):
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
        self.editor.clear()
        self.parse_changes()

    def set_current_theme(self, title):
        style = ""
        for path in self.toolbar.themes_dir.iterdir():
            if path.stem == title:
                data = json.load(open(path))
                style = json_to_stylesheet(data)
        self.editor.setPlainText(style)
        self.parse_changes()

    def preview_style(self, checked):
        ss = QApplication.instance().styleSheet()
        if checked:
            self.current_style = ss
            self.parse_changes()
        else:
            QApplication.instance().setStyleSheet(self.current_style)
            self.current_style = None

    def insert_color(self, color):
        pattern = re.compile(r'#[a-zA-Z0-9]{3,6}\s?;?')
        pattern2 = re.compile(r'\s?rgb\(\d+,\s?\d+,\s?\d+\);?')
        cursor = self.editor.textCursor()
        pos = cursor.position()
        text = self.editor.toPlainText()
        first = max(pos-8, 0)
        second = max(pos-20,0)
        if result := pattern.search(text[first:pos]):
            s, e = first + result.start(), pos
            cursor.movePosition(
                cursor.MoveOperation.Left, cursor.MoveMode.KeepAnchor, e - s
            )
            cursor.deleteChar()
        elif result := pattern2.search(text[second:pos]):
            s, e = second + result.start(), pos
            cursor.movePosition(
                cursor.MoveOperation.Left, cursor.MoveMode.KeepAnchor, e - s
            )
            cursor.deleteChar()
        self.editor.insertPlainText(color + ";")

    def live_update(self):
        if self.toolbar.live_action.isChecked():
            self.parse_changes()

    def parse_changes(self):
        text = self.editor.toPlainText()
        self.apply_stylesheet(text)

    def apply_stylesheet(self, text):
        if not text:
            QApplication.instance().setStyleSheet("")
            return
        parser = QssParser(text)
        if parser.results:
            QApplication.instance().setStyleSheet(text)
