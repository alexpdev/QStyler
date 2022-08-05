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

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QComboBox, QToolBar

from QStyler.actions import EditAction, ShowAction, opengithub, saveQss
from QStyler.utils import get_icon, get_manager


class ThemeCombo(QComboBox):
    """Combo Box for themes."""

    def __init__(self, parent=None):
        """Cunstruct theme combo box."""
        super().__init__(parent=parent)
        self.setEditable(False)
        self.setSizeAdjustPolicy(self.AdjustToContents)
        self._parent = parent
        self.manager = get_manager()
        self.addItem("")
        for name in self.manager.titles:
            self.addItem(name)


class ToolBar(QToolBar):
    """Tool Bar class object."""

    def __init__(self, parent=None):
        """Build the tool bar and it's buttons and widgets."""
        super().__init__(parent=parent)
        self.widget = parent
        self.setMovable(True)
        self.manager = get_manager()
        self.setIconSize(QSize(35, 35))
        self.plus_button_action = QAction()
        self.plus_button_action.setIcon(get_icon("plus"))
        self.minus_button_action = QAction()
        self.minus_button_action.setIcon(get_icon("minus"))
        self.plus_button_action.setToolTip("Add Widget Control Group")
        self.minus_button_action.setToolTip("Remove Widget Control Group")
        self.addAction(self.plus_button_action)
        self.addAction(self.minus_button_action)
        self.addSeparator()
        self.themecombo = ThemeCombo(parent=self)
        self.addWidget(self.themecombo)
        self.apply_theme_action = QAction()
        self.apply_theme_action.setIcon(get_icon("confirm"))
        self.apply_theme_action.setToolTip("Apply Theme")
        self.addAction(self.apply_theme_action)
        self.addSeparator()
        self.view_current_action = ShowAction()
        self.view_current_action.setIcon(get_icon("file"))
        self.view_current_action.setToolTip("View Current Theme")
        self.addAction(self.view_current_action)
        self.edit_theme_action = EditAction()
        self.edit_theme_action.setIcon(get_icon("edit"))
        self.edit_theme_action.setToolTip("Edit Current Theme")
        self.addAction(self.edit_theme_action)
        self.save_current_action = QAction()
        self.save_current_action.setIcon(get_icon("save"))
        self.save_current_action.setToolTip("Save Current Theme To File")
        self.addAction(self.save_current_action)
        self.load_theme_action = QAction()
        self.load_theme_action.setIcon(get_icon("import"))
        self.load_theme_action.setToolTip("Load New Theme From File")
        self.addAction(self.load_theme_action)
        self.addSeparator()
        self.reset_theme_action = QAction()
        self.reset_theme_action.setIcon(get_icon("reset"))
        self.reset_theme_action.setToolTip("Reset Theme")
        self.addAction(self.reset_theme_action)
        self.github_action = QAction()
        self.github_action.setIcon(get_icon("github"))
        self.github_action.setToolTip("Open Github Repo")
        self.addAction(self.github_action)
        self.plus_button_action.triggered.connect(self.widget.add_widget_combo)
        self.minus_button_action.triggered.connect(
            self.widget.minus_widget_combo)
        self.view_current_action.triggered.connect(
            self.view_current_action.showStyles)
        self.github_action.triggered.connect(opengithub)
        self.reset_theme_action.triggered.connect(self.manager.reset)
        self.apply_theme_action.triggered.connect(self.apply_theme)
        self.edit_theme_action.triggered.connect(
            self.edit_theme_action.edit_current_sheet)
        self.save_current_action.triggered.connect(saveQss)

    def activate_load_item(self):
        """
        Activate the load item actions for the toolbar located in menubar.
        """
        loadAction = self.widget.window.menubar.loadAction
        loadAction.loaded.connect(self.load_new_theme)
        self.load_theme_action.triggered.connect(loadAction.trigger)

    def load_new_theme(self, _, title):
        """
        Load and apply the given theme with the title as current theme.

        Parameters
        ----------
        _ : dict
            the theme dictionary
        title : str
            the title of the theme
        """
        self.themecombo.addItem(title)

    def apply_theme(self):
        """
        Apply current value of the manager sheets as the current theme.
        """
        theme = self.themecombo.currentText()
        if not theme:
            self.manager.reset()
        else:
            self.manager.apply_theme(theme)
