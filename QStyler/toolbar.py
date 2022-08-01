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
"""Module for toolbar for styler table."""

from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QToolBar, QComboBox

from QStyler.utils import get_manager, get_icon
from QStyler.actions import ShowAction, EditAction, saveQss


class ThemeCombo(QComboBox):
    """Combo Box for themes."""

    def __init__(self, parent=None):
        """Cunstruct theme combo box."""
        super().__init__(parent=parent)
        self.setEditable(False)
        self._parent = parent
        self.manager = get_manager()
        self.addItem("")
        for name in self.manager.themes.keys():
            self.addItem(name)


class ToolBar(QToolBar):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.manager = get_manager()
        self.themecombo = ThemeCombo(parent=self)
        self.addWidget(self.themecombo)
        self.apply_theme_action = QAction()
        self.apply_theme_action.setIcon(get_icon('confirm'))
        self.apply_theme_action.setToolTip('Apply Theme')
        self.addAction(self.apply_theme_action)
        self.addSeparator()
        self.view_current_action = ShowAction()
        self.view_current_action.setToolTip("View current theme")
        self.view_current_action.setIcon(get_icon("file"))
        self.addAction(self.view_current_action)
        self.save_current_action = QAction()
        self.save_current_action.setToolTip("Save")
        self.save_current_action.setIcon(get_icon("floppy-disk"))
        self.addAction(self.save_current_action)
        self.load_theme_action = QAction()
        self.load_theme_action.setToolTip("Load")
        self.load_theme_action.setIcon(get_icon("import"))
        self.addAction(self.load_theme_action)
        self.reset_theme_action = QAction()
        self.reset_theme_action.setToolTip("Reset")
        self.reset_theme_action.setIcon(get_icon("reset"))
        self.addAction(self.reset_theme_action)
        self.edit_theme_action = EditAction()
        self.edit_theme_action.setIcon(get_icon("edit"))
        self.edit_theme_action.setToolTip("Edit Current Theme")
        self.edit_theme_action.setIcon(get_icon("edit"))
        self.addAction(self.edit_theme_action)
        self.view_current_action.triggered.connect(self.view_current_action.showStyles)
        self.reset_theme_action.triggered.connect(self.manager.reset)
        self.apply_theme_action.triggered.connect(self.apply_theme)
        self.edit_theme_action.triggered.connect(self.edit_theme_action.edit_current_sheet)
        self.save_current_action.triggered.connect(saveQss)

    def activate_load_item(self):
        loadAction = self.parent().window.menubar.loadAction
        loadAction.loaded.connect(self.load_new_theme)
        self.load_theme_action.triggered.connect(loadAction.trigger)

    def load_new_theme(self, theme, title):
        self.themecombo.addItem(title)


    def apply_theme(self):
        theme = self.themecombo.currentText()
        if not theme:
            self.manager.reset()
        else:
            self.manager.apply_theme(theme)
