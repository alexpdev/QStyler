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
"""Module for testing functions and methods."""

import sys

import pytest
from PySide6.QtWidgets import QApplication, QMainWindow

from QStyler.window import MainWindow


@pytest.fixture(scope="module")
def app() -> QApplication:
    """
    Test fixture for QApplication.

    Returns
    -------
    QApplication
        _description_

    Yields
    ------
    Iterator[QApplication]
        _description_
    """
    app = QApplication(sys.argv)
    yield app
    app.quit()
    del app


@pytest.fixture(scope="module")
def window(app: QApplication) -> tuple:
    """
    Test fixture for Application and MainWindow.

    Parameters
    ----------
    app : QApplication
        _description_

    Yields
    ------
    Iterator[tuple]
        _description_
    """
    mainwindow: QMainWindow = MainWindow()
    mainwindow.show()
    yield mainwindow, app


def test_main_window(app: QApplication):
    """
    Test the main window.

    Parameters
    ----------
    app : QApplication
        _description_
    """
    assert app
    mainwindow = MainWindow()
    mainwindow.show()
    assert mainwindow


def test_menu_bar(app: QApplication):
    """
    Test the menu bar.

    Parameters
    ----------
    app : QApplication
        _description_
    """
    assert app
    mainwindow = MainWindow()
    mainwindow.show()
    mainwindow.menubar.fileMenu.showStyles()
    assert mainwindow


def test_styler_widget_combo(window: tuple):
    """
    Test the styler tab widget combo box.

    Parameters
    ----------
    window : tuple
        _description_
    """
    app: QApplication = window[1]
    window: QMainWindow = window[0]
    assert app
    window.tabWidget.setCurrentIndex(2)
    app.processEvents()
    tab = window.styler
    tab.widget_combo.setCurrentIndex(5)
    text = tab.widget_combo.currentText()
    assert text in tab.lineedit.text()


def test_apply_theme(window: tuple):
    """
    Test applying theme.

    Parameters
    ----------
    window : tuple
        _description_
    """
    app: QApplication = window[1]
    window: QMainWindow = window[0]
    assert app
    window.tabWidget.setCurrentIndex(2)
    app.processEvents()
    for k in window.menubar.optionsMenu.themeactions:
        k.trigger()
        break
    tab = window.styler
    for i in range(tab.widget_combo.count()):
        text = tab.widget_combo.itemText(i)
        if text == "QPushButton":
            break
    text = tab.widget_combo.setCurrentIndex(i)
    assert tab.table.rowCount() > 1
