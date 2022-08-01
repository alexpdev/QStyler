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
import os
from copy import deepcopy
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication


class Memo:
    """Memoize data."""

    def __init__(self, func):
        """Initialize the class instance."""
        self.cache = {}
        self.func = func

    def __call__(self, *args, **kwargs):
        """Invoke function call and save results to cache."""
        if args in self.cache:
            return self.cache[args]
        result = self.func(*args, **kwargs)
        self.cache[args] = result
        return result


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


@Memo
def load_records(filename):
    """Return data regarding QWidgets and styles."""
    path = get_src_dir() / "style" / filename

    return json.load(open(path, encoding="utf-8"))


def get_manager():
    """Get the manager from any module."""
    return Application.instance().manager


class StyleManager:
    """Style Sheet Manager."""

    def __init__(self):
        """Initialize the Style Factory class."""
        self.themes = load_records("themes.json")
        self.data = load_records("data.json")
        self.extras = []
        self.app = QApplication.instance()
        self.sheets = []

    def get_theme(self, name: str) -> dict:
        """Return the theme associated with the given name."""
        if name in self.themes:
            return self.themes[name]
        return {}

    @staticmethod
    def convert_to_sheets(theme: dict) -> list:
        """Convert dictionary theme to sheets."""
        sheets = []
        for key, value in theme.items():
            sheet = {key: value}
            sheets.append(sheet)
        return sheets

    def append_sheet(self, widget: str, prop: str, value: str):
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
        widgets = widget.split(",")
        for sheet in self.sheets:
            widg = next(iter(sheet.keys()))
            if widg in widgets:
                sheet[widg].update({prop: value})
                widgets.remove(widg)
        self.sheets += [{widget: {prop: value}} for widget in widgets]
        self.update_theme()

    def _create_ssheet(self, sheets=None) -> dict:
        """
        Update the sheet with data from table.

        Returns
        -------
        dict
            the changed sheet
        """
        ssheet = ""
        if not sheets:
            sheets = self.sheets
        for row in sheets:
            for k, v in row.items():
                ssheet += k + " {\n"
                for key, val in v.items():
                    ssheet += "    " + key + ": " + val + ";\n"
                ssheet += "}\n"
        return ssheet

    def update_theme(self):
        """Apply current sheet to widget."""
        ssheet = self._create_ssheet()
        self.app.setStyleSheet(ssheet)

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
        if not widget:
            return {}
        widgets = widget.split(",")
        styles = {}
        for sheet in self.sheets:
            for widg in widgets:
                if widg in sheet:
                    styles[widg] = sheet[widg]
                    widgets.remove(widg)
                    break
        if len(widgets) >= 1:
            return {}
        seq = iter(styles.values())
        first = next(seq)
        for sheet in seq:
            if not first:
                return {}
            for key, value in sheet.items():
                if key in first and value != first[key]:
                    del first[key]
        return first

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

    def reset(self):
        """Reset the current theme to default."""
        self.sheets = []
        self.update_theme()

    def apply_theme(self, name):
        """Apply given theme as current theme."""
        theme = self.themes[name]
        sheets = self.convert_to_sheets(theme)
        self.sheets = sheets
        self.update_theme()


class QssParser:
    """Qt Style Sheet Parser."""

    def __init__(self, path):
        """
        Initialize and construct the qss parser object.

        Parameters
        ----------
        path : str
            path to qss file
        """
        if not isinstance(path, str) or os.path.exists(path):
            with open(path, "rt", encoding="utf-8") as fd:
                content = fd.read().split("\n")
        else:
            content = path.split("\n")
        self.lines = content
        self.result = {}
        self.collection = []
        self.lnum = 0
        self.total = len(self.lines)
        self.parse_qss()

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

    @staticmethod
    def serialize_prop(line):
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
            key, val = group[0].strip(), ":".join(group[1:]).strip()
            if val.endswith(";"):
                val = val[:-1]
            return {key: val}
        except IndexError:  # pragma: nocover
            return None

    def parse_qss(self):
        """
        Parse the content of the qss file one line at a time.
        """
        inblock = False
        widgets, props = [], {}
        while self.lnum < self.total:
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
                    if prop:
                        props.update(prop)
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
                if prop:
                    props.update(prop)
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


class Application(QApplication):
    """Subclass of the QApplication."""

    def __init__(self, *args, **kwargs):
        """Initialize application."""
        super().__init__(*args, **kwargs)
        self.manager = StyleManager()
