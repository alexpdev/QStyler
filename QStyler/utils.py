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
"""Utility module."""

import json
from pathlib import Path
from copy import deepcopy

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication


class Lorem:
    """Generator of standard lorem ipsum dummy text."""

    def __init__(self):
        """Initialize the Lorem class."""
        self.text = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
            "do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco "
            "laboris nisi ut aliquip ex ea commodo consequat. Duis aute "
            "irure dolor in reprehenderit in voluptate velit esse cillum "
            "dolore eu fugiat nulla pariatur. Excepteur sint occaecat "
            "cupidatat non proident, sunt in culpa qui officia deserunt "
            "mollit anim id est laborum."
        )
        self.words = self.text.split(" ")
        self.it = self.iternext()

    def iternext(self):
        """Generate words forever."""
        while True:
            for word in self.words:
                yield word

    def gentext(self):
        """Return lorem text."""
        return self.text

    def genword(self):
        """Return a single word from text."""
        return next(self.it)


def exitApp():  # pragma: nocover
    """Quit the application."""
    qapp = QApplication.instance()
    qapp.quit()


def get_src_dir():
    """Return the source directory."""
    return Path(__file__).resolve().parent


def get_window_icon(filename=None):
    """Get the path to the window icon."""
    path = get_src_dir().parent
    if not filename:
        iconpath = path / "assets" / "QStylerIcon.png"
    else:
        iconpath = path / "assets" / filename
    return QIcon(str(iconpath))


def load_records(filename):
    """Return data regarding QWidgets and styles."""
    path = get_src_dir() / "style" / filename
    records = json.load(open(path, encoding="utf-8"))
    return records


class StyleManager:
    """
    Style Factory for table widget.
    """

    def __init__(self):
        """
        Initialize the Style Factory class.
        """
        self.themes = load_records('themes.json')
        self.data = load_records('data.json')
        self.app = QApplication.instance()
        self.sheets = []

    def addSheet(self, widget: object, prop: str, value: str):
        """
        Add sheet data for widget to list of stylesheets.

        Parameters
        ----------
        widget : QWidget
            _description_
        prop : str
            _description_
        value : str
            _description_
        """
        for sheet in self.sheets:
            if widget in sheet:
                sheet[widget][prop] = value
                break
        else:
            self.sheets.append({widget: {prop: value}})
        self._apply_ssheet()

    def _apply_ssheet(self) -> dict:
        """
        Update the sheet with data from table.

        Returns
        -------
        dict
            the changed sheet
        """
        ssheet = ""
        for row in self.sheets:
            for k, v in row.items():
                ssheet += k + " {\n"
                for key, val in v.items():
                    ssheet += "    " + key + ": " + val + ";\n"
                ssheet += "}\n"
        self.app.setStyleSheet(ssheet)
        return ssheet

    def get_sheet(self, widget: str) -> dict:
        """
        Get the sheet associated with the widget or empty dict.

        Parameters
        ----------
        widget : str
            The name of the widget to get the sheet for.

        Returns
        -------
        dict
            Empty dict or current style sheet.
        """
        if widget:
            for sheet in self.sheets:
                if widget in sheet:
                    return sheet[widget]
        return {}

    def saveToFile(self, path: str) -> None:
        """
        Save current style sheet.

        Parameters
        ----------
        path : str
            path to save file.
        """
        stylesheet = self._apply_ssheet()
        with open(path, "wt", encoding="utf-8") as fd:
            fd.write(stylesheet)

    def sanatize_prop(self, prop):
        """Sanatize property text."""
        prop = prop.strip()
        lst = prop.strip(":")
        try:
            properte, value = lst[0], ":".join(lst[1:])
            if value[-1] == ";":
                value = value[:-1]
            return properte.strip(), value.strip()
        except IndexError:
            pass


    def parse(self):
        """Parse lines from file."""
        start = 0
        while start < self.size:
            start += 1
            states = []
            while "{" not in self.lines[start]:
                states.append(self.lines[start])
                start += 1
            states.append(self.lines[start][:self.lines[start].index("{")])
            props = {}
            start += 1
            while "}" not in self.lines[start]:
                prop, value = self.sanatize_props()
                props[prop] = value
                start += 1
            widgets = [i.strip() for i in ''.join(states).split(',')]
            for widget in widgets:
                self.out.append({widget: deepcopy(props)})
            start += 1
        return

def blockSignals(func):
    """
    Decorate for blocking signals in decorated functions.

    Parameters
    ----------
    func : Callable
        function wrapped
    """

    def wrapper(widget, *args, **kwargs):
        """
        Wrap function with functionality.

        Parameters
        ----------
        widget : QWidget
            the QWidget instance.

        Returns
        -------
        any
            the return value of wrapped function.
        """
        widget.blockSignals(True)
        result = func(widget, *args, **kwargs)
        widget.blockSignals(False)
        return result

    return wrapper
