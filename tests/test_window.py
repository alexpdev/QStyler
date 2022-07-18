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

import os
import sys
import time

import pytest
from PySide6.QtWidgets import QApplication, QMainWindow

from QStyler import __main__, version
from QStyler.utils import StyleManager
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
    app = QApplication(sys.argv)
    mainwindow: QMainWindow = MainWindow()
    mainwindow.show()
    yield mainwindow, app
    app.quit()


def processtime(app):
    """Process Events and sleep for a second."""
    app.processEvents()
    time.sleep(0.02)


def test_main_entry():
    """Test __main__ module can be imported without harm."""
    assert __main__


def test_version():
    """Test version module."""
    assert isinstance(version.__version__, str)


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
    processtime(pre[1])
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
    processtime(app)
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
    window, app = pre
    window.tabWidget.setCurrentIndex(0)
    processtime(app)
    theme = next(iter(window.menubar.optionsMenu.themeactions))
    theme.trigger()
    processtime(app)
    tab = window.styler
    for i in range(tab.widget_combo.count()):
        text = tab.widget_combo.itemText(i)
        if text == "QPushButton":
            break
    processtime(app)
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
    window, app = pre
    window.tabWidget.setCurrentIndex(0)
    processtime(app)
    tab = window.styler
    for i in range(tab.widget_combo.count()):
        text = tab.widget_combo.itemText(i)
        if text == "QLineEdit":
            tab.widget_combo.setCurrentIndex(i)
            break
    processtime(app)
    propcombo = tab.table.cellWidget(0, 0)
    for j in range(propcombo.count()):
        if propcombo.itemText(j) == "background-color":
            propcombo.setCurrentIndex(j)
            tab.table.item(0, 1).setText("#000")
            break
    processtime(app)
    assert tab.table.item(0, 1).text() == "#000"
    assert tab.table.rowCount() > 1


def test_reset_property(pre: tuple):
    """
    Test applying theme.

    Parameters
    ----------
    window : tuple
    """
    app: QApplication = pre[1]
    window: QMainWindow = pre[0]
    window.tabWidget.setCurrentIndex(0)
    processtime(app)
    tab = window.styler
    for i in range(tab.widget_combo.count()):
        text = tab.widget_combo.itemText(i)
        if text == "QComboBox":
            tab.widget_combo.setCurrentIndex(i)
            break
    processtime(app)
    propcombo = tab.table.cellWidget(0, 0)
    for j in range(propcombo.count()):
        if propcombo.itemText(j) == "border-color":
            propcombo.setCurrentIndex(j)
            tab.table.item(0, 1).setText("#000")
            break
    processtime(app)
    assert tab.table.item(0, 1).text() == "#000"
    theme = next(iter(window.menubar.optionsMenu.themeactions))
    theme.trigger()
    processtime(app)
    for i in range(tab.widget_combo.count()):
        text = tab.widget_combo.itemText(i)
        if text == "QComboBox":
            break
    processtime(app)
    text = tab.widget_combo.setCurrentIndex(i)
    window.menubar.optionsMenu.resetAction.trigger()
    processtime(app)
    assert tab.table.rowCount() > 1


def test_style_table_props(pre: tuple):
    """Test the props combos in the style table."""
    window, app = pre
    actions = window.menubar.optionsMenu.themeactions
    window.tabWidget.setCurrentIndex(1)
    processtime(app)
    first_theme = next(iter(actions))
    first_theme.trigger()
    processtime(app)
    styler = window.styler
    styler.widget_combo.setCurrentText("QLineEdit")
    processtime(app)
    window.tabWidget.setCurrentIndex(2)
    processtime(app)
    styler.table.cellWidget(0, 0).setCurrentText("color")
    styler.table.item(0, 1).setText("#F00")
    processtime(app)
    styler.checkbox.toggle()
    processtime(app)
    assert styler.checkbox.isChecked()


def test_tickers(pre: tuple):
    """Test the tickers in slider widgets."""
    window, app = pre
    window.tabWidget.setCurrentIndex(1)
    processtime(app)
    window.tabWidget.setCurrentIndex(0)
    processtime(app)
    tab = window.widgets
    val1 = tab.verticalSlider.value()
    val2 = tab.horizontalSlider.value()
    print(val1, val2)
    while tab.verticalSlider.value() < 99:
        tab.verticalSlider.triggerAction(
            tab.verticalSlider.SliderSingleStepAdd
        )
        tab.horizontalSlider.triggerAction(
            tab.horizontalSlider.SliderSingleStepAdd
        )
        processtime(app)
    assert tab.verticalSlider.value() > 95
    assert tab.horizontalSlider.value() > 95


def test_load_qss():
    """Test stylesheet parser."""
    testdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(testdir, "test.qss"), encoding="utf-8") as fd:
        text = fd.read()
    manager = StyleManager()
    out = manager.parse(text)
    assert len(out) == 3
