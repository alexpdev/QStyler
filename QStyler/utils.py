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
import webbrowser

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication


class ParsingError(Exception):
    pass


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
def load_theme(title):
    """Return data regarding QWidgets and styles."""
    path = get_src_dir() / "themes" / (title + ".json")
    return json.load(open(path, encoding="utf-8"))


def json_to_stylesheet(theme: dict) -> str:
    ssheet = ""
    for k, v in theme.items():
        if not k or not v:
            continue  # pragma: nocover
        ssheet += k + " {\n"
        for key, val in v.items():
            ssheet += "    " + key + ": " + val + ";\n"
        ssheet += "}\n"
    return ssheet

class QssParser:
    """Qt Style Sheet Parser."""

    def __init__(self, path_or_string=None):
        """
        Initialize and construct the qss parser object.
        """
        self._line = 0
        self._total = 0
        self._lines = []
        self.results = {}
        self.collection = []
        if path_or_string is not None:
            self.parse(path_or_string)

    def parse(self, path_or_string):
        """
        Parse the style sheet and convert it to json, and dictionary styled.

        Parameters
        ----------
        path_or_string : str
            either the path to the file or a string containing stylesheets.
        """
        self._clear()
        if os.path.exists(path_or_string):
            with open(path_or_string, "rt", encoding="utf-8") as fd:
                self._lines = [i.strip() for i in fd.read().split("\n")]
        else:
            self._lines = [i.strip() for i in path_or_string.split("\n")]
        self._total = len(self._lines)
        try:
            self._parse_qss()
        except IndexError:
            if hasattr(self, "_line"):
                raise ParsingError(str(self._line))
        self._compile()
        return self.results

    def _clear(self):
        """Clear any previous data from last parse."""
        self._line = self._total = 0
        self._lines, self.collection = [], []
        self.results = {}

    @property
    def current(self):
        """
        Return the current line.

        Returns
        -------
        str
            The current line
        """
        return self._lines[self._line]

    def _skipcomment(self):
        """
        Skip all lines until parser reaches the end comment token.
        """
        while "*/" not in self.current:
            self._line += 1
        self._line += 1

    def _add_widgets(self, widgets, props):
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
            try:
                self.collection.append({widget.strip(): deepcopy(props)})
            except IndexError:
                return

    @staticmethod
    def _serialize_prop(line):
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
            if "url" in val:
                return {}
            if val.endswith(";"):
                val = val[:-1]
            return {key: val}
        except IndexError:  # pragma: nocover
            return {}

    def _parse_qss(self):
        """
        Parse the content of the qss file one line at a time.
        """
        inblock = False
        widgets, props = [], {}
        while self._line < self._total:
            if self.current == "":
                self._line += 1
                continue
            if "/*" in self.current:
                self._skipcomment()
                continue
            if "{" in self.current:
                sblock = self.current.index("{")
                widgets.append(self.current[:sblock])
                if "}" in self.current:
                    eblock = self.current.index("}")
                    prop = self.current[sblock+1:eblock]
                    prop = self._serialize_prop(prop)
                    if prop:
                        props.update(prop)
                    self._add_widgets(widgets, props)
                    widgets, props = [], {}
                    self._line += 1
                    continue
                self._line += 1
                inblock = True
                continue
            if "}" in self.current:
                inblock = False
                self._add_widgets(widgets, props)
                self._line += 1
                widgets, props = [], {}
                continue
            if inblock:
                parts = []
                while ";" not in self.current:
                    parts.append(self.current.strip())
                    self._line += 1
                parts.append(self.current.strip())
                prop = self._serialize_prop(" ".join(parts))
                if prop:
                    props.update(prop)
                self._line += 1
                continue
            widgets.append(self.current)
            self._line += 1

    def _compile(self):
        """
        Gather and group all results into one dictionary.
        """
        for row in self.collection:
            self.results.update(row)


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

def open_github_browser():
    webbrowser.open("https://github.com/alexpdev/QStyler")

def apply_stylesheet(text):
    if not text:
        QApplication.instance().setStyleSheet("")
        return
    parser = QssParser(text)
    if parser.results:
        QApplication.instance().setStyleSheet(text)
