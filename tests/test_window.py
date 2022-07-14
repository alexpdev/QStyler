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
import time

import pytest
from PySide6.QtWidgets import QApplication, QMainWindow

from QStyler.window import MainWindow


@pytest.fixture(scope="module")
def pre() -> tuple:
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
    app = QApplication()
    mainwindow: QMainWindow = MainWindow()
    mainwindow.show()
    yield mainwindow, app
    app.quit()


def test_main_window(pre: tuple):
    """
    Test the main window.

    Parameters
    ----------
    pre: tuple
        the app and window.
    """
    assert pre[0]
    assert pre[1]


def test_menu_bar(pre: tuple):
    """
    Test the menu bar.

    Parameters
    ----------
    pre: tuple
        the app and window.
    """
    assert pre
    pre[1].processEvents()
    time.sleep(0.01)
    assert pre[0]


def test_styler_widget_combo(pre: tuple):
    """
    Test the styler tab widget combo box.

    Parameters
    ----------
    window : tuple
        _description_
    """
    app: QApplication = pre[1]
    window: QMainWindow = pre[0]
    assert app
    window.tabWidget.setCurrentIndex(2)
    app.processEvents()
    time.sleep(0.01)
    tab = window.styler
    tab.widget_combo.setCurrentIndex(5)
    text = tab.widget_combo.currentText()
    assert text in tab.lineedit.text()


def test_apply_theme(pre: tuple):
    """
    Test applying theme.

    Parameters
    ----------
    window : tuple
        _description_
    """
    app: QApplication = pre[1]
    window: QMainWindow = pre[0]
    app.processEvents()
    time.sleep(0.01)
    assert app
    window.tabWidget.setCurrentIndex(2)
    app.processEvents()
    time.sleep(0.01)
    for k in window.menubar.optionsMenu.themeactions:
        k.trigger()
        break
    app.processEvents()
    time.sleep(0.01)
    tab = window.styler
    for i in range(tab.widget_combo.count()):
        text = tab.widget_combo.itemText(i)
        if text == "QPushButton":
            break
    app.processEvents()
    time.sleep(0.01)
    text = tab.widget_combo.setCurrentIndex(i)
    assert tab.table.rowCount() > 1


def test_set_property(pre: tuple):
    """
    Test applying theme.

    Parameters
    ----------
    window : tuple
        _description_
    """
    app: QApplication = pre[1]
    window: QMainWindow = pre[0]
    assert app
    window.tabWidget.setCurrentIndex(2)
    app.processEvents()
    time.sleep(0.01)
    tab = window.styler
    for i in range(tab.widget_combo.count()):
        text = tab.widget_combo.itemText(i)
        if text == "QPushButton":
            tab.widget_combo.setCurrentIndex(i)
            break
    app.processEvents()
    app.processEvents()
    time.sleep(0.01)
    propcombo = tab.table.cellWidget(0, 0)
    for j in range(propcombo.count()):
        if propcombo.itemText(j) == "background-color":
            propcombo.setCurrentIndex(j)
            tab.table.item(0, 1).setText("#000")
            break
    app.processEvents()
    time.sleep(0.01)
    assert tab.table.item(0, 1).text() == "#000"
    assert tab.table.rowCount() > 1


def test_reset_property(pre: tuple):
    """
    Test applying theme.

    Parameters
    ----------
    window : tuple
        _description_
    """
    app: QApplication = pre[1]
    window: QMainWindow = pre[0]
    assert app
    window.tabWidget.setCurrentIndex(2)
    app.processEvents()
    time.sleep(0.01)
    tab = window.styler
    for i in range(tab.widget_combo.count()):
        text = tab.widget_combo.itemText(i)
        if text == "QPushButton":
            tab.widget_combo.setCurrentIndex(i)
            break
    app.processEvents()
    time.sleep(0.01)
    app.processEvents()
    propcombo = tab.table.cellWidget(0, 0)
    for j in range(propcombo.count()):
        if propcombo.itemText(j) == "background-color":
            propcombo.setCurrentIndex(j)
            tab.table.item(0, 1).setText("#000")
            break
    app.processEvents()
    time.sleep(0.01)
    assert tab.table.item(0, 1).text() == "#000"
    for k in window.menubar.optionsMenu.themeactions:
        k.trigger()
        break
    app.processEvents()
    time.sleep(0.01)
    tab = window.styler
    for i in range(tab.widget_combo.count()):
        text = tab.widget_combo.itemText(i)
        if text == "QPushButton":
            break
    app.processEvents()
    time.sleep(0.01)
    text = tab.widget_combo.setCurrentIndex(i)
    window.menubar.optionsMenu.resetAction.trigger()
    app.processEvents()
    time.sleep(0.01)
    assert tab.table.rowCount() > 1
