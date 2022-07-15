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


def getsrcdir():
    """Return the source directory."""
    return Path(__file__).resolve().parent


def geticon():
    """Get the path to the window icon."""
    path = getsrcdir().parent
    iconpath = path / "assets" / "QStylerIcon.png"
    return QIcon(str(iconpath))


def getdata():
    """Return data regarding QWidgets and styles."""
    path = getsrcdir() / "style" / "data.json"
    data = json.load(open(path, encoding="utf-8"))
    return data
