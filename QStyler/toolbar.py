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

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QToolBar, QToolButton, QComboBox

from QStyler.utils import get_manager


class ThemeCombo(QComboBox):
    """Combo Box for themes."""

    def __init__(self, parent=None):
        """Cunstruct theme combo box."""
        super().__init__(parent=parent)
        self.setEditable(False)
        self._parent = parent
        self.manager = get_manager()
        self.currentIndexChanged()
        self.addItem("")
        for name in self.manager.themes.keys():
            self.addItem(name)

    def apply_theme(self):
        name = self.currentText()
        if name:
            theme = self.manager[name]
            self.manager.apply_theme(theme)



class ToolBar(QToolBar):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
