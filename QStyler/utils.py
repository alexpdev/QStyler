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
from copy import deepcopy
from pathlib import Path

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
            "mollit anim id est laborum.")
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


def get_icon(filename=None):
    """Get the path to the window icon."""
    path = get_src_dir() / "icons" / filename
    return QIcon(str(path))


def load_records(filename):
    """Return data regarding QWidgets and styles."""
    path = get_src_dir() / "style" / filename

    return json.load(open(path, encoding="utf-8"))


class StyleManager:
    """Style Factory for table widget."""

    def __init__(self):
        """
        Initialize the Style Factory class.
        """
        self.themes = load_records("themes.json")
        self.data = load_records("data.json")
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
        self.set_sheet()

    def _create_ssheet(self) -> dict:
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
        return ssheet

    def set_sheet(self):
        """Apply current sheet to widget."""
        ssheet = self._create_ssheet()
        self.app.setStyleSheet(ssheet)

    def get_style_sheet(self):
        """Return the full style sheet as a string."""
        return self._create_ssheet()  # pragma: nocover

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

    def saveToFile(self, path: str) -> None:  # pragma: nocover
        """
        Save current style sheet.

        Parameters
        ----------
        path : str
            path to save file.
        """
        stylesheet = self._create_ssheet()
        with open(path, "wt", encoding="utf-8") as fd:
            fd.write(stylesheet)


class QssParser:

    def __init__(self, path):
        with open(path, "rt", encoding="utf-8") as fd:
            content = fd.read()
        self.content = content
        self.result = []
        self.line = 0
        self.lines = self.content.split("\n")
        self.total = len(self.lines)
        self.parse()

    def skip_comments(self):
        """Skip over inline comments."""
        while not self.current.endswith("*/"):
            self.line += 1
        self.line += 1

    @property
    def current(self):
        """Return current line."""
        return self.lines[self.line]

    def nextline(self):
        """Increment current by one."""
        self.line += 1
        if self.line >= self.total:
            return False
        return True


    def parse(self):
        """Parse lines from file."""
        while self.line < self.total:
            widgets = []
            if self.current.startswith("/*"):
                self.skip_comments()
                continue
            if not self.current:
                if not self.nextline():
                    return
                continue
            while "{" not in self.current:
                widgets.append(self.current)
                if not self.nextline():
                    return self.result
            widgets.append(self.current[:self.current.index("{")])
            props = {}
            if not self.nextline():
                return self.result
            while "}" not in self.current:
                result = self.sanatize_prop()
                if result:
                    prop, value = result
                    props[prop] = value
                if not self.nextline():
                    return self.result
            if not self.nextline():
                return self.result
            widgets = [i.strip() for i in "".join(widgets).split(",")]
            for widget in widgets:
                self.result.append({widget: deepcopy(props)})
            if not self.nextline:
                return self.result
        return self.result

    def sanatize_prop(self):
        """Sanatize property text."""
        lst = self.current.strip().split(":")
        try:
            prop, value = lst[0].strip(), ":".join(lst[1:])
            if value[-1] == ";":
                value = value[:-1]
            return prop, value.strip()
        except IndexError:
            return None


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
