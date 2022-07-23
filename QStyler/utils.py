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
    """Qt Style Sheet Parser"""

    def __init__(self, path):
        """
        Initialize and construct the qss parser object.

        Parameters
        ----------
        path : str
            path to qss file
        """
        with open(path, "rt", encoding="utf-8") as fd:
            content = fd.read().split("\n")
        self.lines = content
        self.result = {}
        self.collection = []
        self.lnum = 0
        self.total = len(self.lines)
        self.parse()

    @property
    def current(self):
        """
        Return the current line.

        Returns
        -------
        str
            The current line
        """
        return self.lines[self.lnum]

    def skipcomment(self):
        """
        Skip all lines until parser reaches the end comment token.
        """
        while "*/" not in self.current:
            self.lnum += 1
        self.lnum += 1

    def add_widgets(self, widgets, props):
        """
        Add widgets to the the master collection.

        Parameters
        ----------
        widgets : str
            The widgets name
        props : dict
            the property names and values
        """
        widget_str = "".join(widgets)
        widgets = widget_str.split(",")
        for widget in widgets:
            self.collection.append({widget.strip(): deepcopy(props)})

    def serialize_prop(self, line):
        """
        Normalize property string into name and value.

        Parameters
        ----------
        line : str
            the current line

        Returns
        -------
        dict
            the key,value pair of the normalized results
        """
        try:
            group = line.split(":")
            key, val = group[0].strip(), ':'.join(group[1:]).strip()
            if val.endswith(";"):
                val = val[:-1]
            return {key: val}
        except IndexError:
            return None

    def parse_qss(self):
        """
        Parse the content of the qss file one line at a time.
        """
        inblock = False
        widgets, props = [], {}
        while self.location < self.total:
            if self.current == "":
                self.lnum += 1
                continue
            if "/*" in self.current:
                self.skipcomment()
                continue
            if "{" in self.current:
                sblock = self.current.index("{")
                widgets.append(self.current[:sblock])
                if "}" in self.current:
                    eblock = self.current.index("}")
                    prop = self.current[sblock:eblock]
                    prop = self.serialize_prop(prop)
                    if prop: props.update(prop)
                    self.add_widgets(widgets, props)
                    widgets, props = [], {}
                    self.lnum += 1
                    continue
                self.lnum += 1
                inblock = True
                continue
            if "}" in self.current:
                inblock = False
                self.add_widgets(widgets, props)
                self.lnum += 1
                widgets, props = [], {}
                continue
            if inblock:
                prop = self.serialize_prop(self.current)
                if prop: props.update(prop)
                self.lnum += 1
                continue
            widgets.append(self.current)
            print(self.current)
            self.lnum += 1
        self.add_widgets(widgets, props)

    def compile(self):
        """
        Gather and group all results into one dictionary.
        """
        for row in self.collection:
            self.result.update(row)


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
