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
from QStyler.utils import QssParser, StyleManager, get_manager
from QStyler.window import Application, MainWindow


@pytest.fixture(scope="package")
def app() -> QApplication:
    """
    Test fixture for Application.

    Yields
    ------
    QApplication
        The main app.
    """
    appl = Application(sys.argv)
    yield appl
    appl.quit()


@pytest.fixture(scope="package")
def wind(app) -> QMainWindow:
    """
    Create a MainWindow object.

    Parameters
    ----------
    app : QApplication
        the application instance.

    Yields
    ------
    Iterator[QMainWindow]
        The main window instance.
    """
    _ = app
    window = MainWindow()
    yield window
    window.close()
    window.deleteLater()


def processtime(app=None):
    """Process Events and sleep for a second."""
    app = app if app else QApplication.instance()
    app.processEvents()
    time.sleep(0.06)


def test_main_entry():
    """Test __main__ module can be imported without harm."""
    assert __main__


def test_version():
    """Test version module."""
    assert isinstance(version.__version__, str)


def test_main_window(wind):
    """
    Test the main window.

    Parameters
    ----------
    wind: QMainWindow
        the window instance.
    """
    assert hasattr(wind, "layout")
    assert hasattr(wind, "central")


def test_menu_bar(wind):
    """
    Test the menu bar.

    Parameters
    ----------
    pre: tuple
        the app and window.
    """
    assert wind


def test_plus_button(wind):
    """
    Test the styler tab widget combo box.

    Parameters
    ----------
    window : tuple
        _description_
    """
    window = wind
    window.tabWidget.setCurrentIndex(2)
    processtime()
    tab = window.styler
    toolbar = tab.toolbar
    tab.combo.setCurrentIndex(5)
    toolbar.plus_button_action.trigger()
    assert len(tab.boxgroups) > 0
    toolbar.minus_button_action.trigger()
    assert len(tab.boxgroups) == 0


def test_apply_theme(wind):
    """
    Test applying theme.

    Parameters
    ----------
    window : tuple
        _description_
    """
    window = wind
    window.tabWidget.setCurrentIndex(0)
    processtime()
    theme = next(iter(window.menubar.optionsMenu.themeactions))
    theme.trigger()
    processtime()
    tab = window.styler
    for i in range(tab.combo.count()):
        text = tab.combo.itemText(i)
        if text == "QPushButton":
            break
    processtime()
    text = tab.combo.setCurrentIndex(i)
    assert tab.table.rowCount() > 1


def test_set_property(wind):
    """
    Test applying theme.

    Parameters
    ----------
    window : QMainWindow
        The MainWindow instance
    """
    window = wind
    window.tabWidget.setCurrentIndex(1)
    processtime()
    tab = window.styler
    for i in range(tab.combo.count()):
        text = tab.combo.itemText(i)
        if text == "QLineEdit":
            tab.combo.setCurrentIndex(i)
            break
    processtime()
    propcombo = tab.table.cellWidget(0, 0)
    for j in range(propcombo.count()):
        if propcombo.itemText(j) == "background-color":
            propcombo.setCurrentText("backround")
            propcombo.setCurrentIndex(j)
            tab.table.item(0, 1).setText("#000")
            break
    processtime()
    assert tab.table.item(0, 1).text() == "#000"
    assert tab.table.rowCount() > 1


def test_reset_property(wind):
    """
    Test applying theme.

    Parameters
    ----------
    window : tuple
    """
    window: QMainWindow = wind
    window.tabWidget.setCurrentIndex(1)
    processtime()
    tab = window.styler
    for i in range(tab.combo.count()):
        text = tab.combo.itemText(i)
        if text == "QComboBox":
            tab.combo.setCurrentIndex(i)
            break
    processtime()
    propcombo = tab.table.cellWidget(0, 0)
    for j in range(propcombo.count()):
        if propcombo.itemText(j) == "border-color":
            propcombo.setCurrentIndex(j)
            tab.table.item(0, 1).setText("#000")
            break
    processtime()
    assert tab.table.item(0, 1).text() == "#000"
    theme = next(iter(window.menubar.optionsMenu.themeactions))
    theme.trigger()
    processtime()
    for i in range(tab.combo.count()):
        text = tab.combo.itemText(i)
        if text == "QSpinBox":
            break
    processtime()
    text = tab.combo.setCurrentIndex(i)
    window.menubar.optionsMenu.resetAction.trigger()
    processtime()
    assert tab.table.rowCount() > 1


def test_style_table_props(wind, app):
    """Test the props combos in the style table."""
    window = wind
    actions = window.menubar.optionsMenu.themeactions
    window.tabWidget.setCurrentIndex(1)
    processtime(app)
    first_theme = next(iter(actions))
    first_theme.trigger()
    processtime(app)
    styler = window.styler
    styler.combo.setCurrentText("QLineEdit")
    processtime(app)
    window.tabWidget.setCurrentIndex(2)
    processtime(app)
    styler.table.cellWidget(0, 0).setCurrentText("color")
    styler.table.item(0, 1).setText("#F00")
    assert "color: #F00;" in app.styleSheet()


def test_tickers(wind):
    """Test the tickers in slider widgets."""
    window = wind
    window.tabWidget.setCurrentIndex(0)
    window.tabWidget.setCurrentIndex(0)
    processtime()
    tab = window.widgets
    while tab.verticalSlider.value() < 99:
        tab.verticalSlider.triggerAction(
            tab.verticalSlider.SliderSingleStepAdd
        )
        tab.horizontalSlider.triggerAction(
            tab.horizontalSlider.SliderSingleStepAdd
        )
        processtime()
    assert tab.verticalSlider.value() > 95
    assert tab.horizontalSlider.value() > 95


@pytest.mark.parametrize("path", [True, False])
def test_load_qss(path):
    """Test stylesheet parser."""
    testdir = os.path.dirname(os.path.abspath(__file__))
    if path:
        text = os.path.join(testdir, "test.qss")
    else:
        with open(os.path.join(testdir, "test.qss"), encoding="utf-8") as fd:
            text = fd.read()
    manager = QssParser(text)
    manager.compile()
    out = manager.result
    assert len(out) == 7


# def test_get_theme_file(wind):
#     """Test get theme file method."""
#     wind.tabWidget.setCurrentIndex(0)
#     testdir = os.path.dirname(os.path.abspath(__file__))
#     path = os.path.join(testdir, "test.qss")
#     qty = len(wind.menubar.optionsMenu.themeMenu.actions())
#     wind.menubar.optionsMenu.getThemeFile("test", path)
#     processtime()
#     assert qty < len(wind.menubar.optionsMenu.themeMenu.actions())


def test_validator_combo(wind):
    """Test the combo validator."""
    wind.tabWidget.setCurrentIndex(1)
    processtime()
    combo = wind.styler.combo
    combo.setCurrentText("QPushButton")
    processtime()
    combo.setCurrentText("QTableWidget")
    processtime()
    combo.setCurrentText("QTableWidget ")
    processtime()
    combo.setCurrentText("QTableWidget Fork")
    processtime()
    combo.setCurrentText("QTableWidget QLineEdit")
    processtime()
    wind.styler.state_combo.loadStates("QTableWidget QLineEdit")
    processtime()
    wind.styler.control_combo.loadControls("QTableWidget QLineEdit")
    assert combo.currentText() == "QTableWidget QLineEdit"


def test_combo_validator(wind):
    """Test combo validator widget."""
    wind.tabWidget.setCurrentIndex(1)
    processtime()
    wind.styler.combo.setCurrentText("QWidg")
    wind.styler.combo.validator().validate("QWidg")
    processtime()
    wind.styler.combo.setCurrentText("QWidgt QLineEdit")
    wind.styler.combo.validator().validate("QWidgt QLineEdit")
    processtime()
    wind.styler.combo.setCurrentText("QWidg ")
    wind.styler.combo.validator().validate("QWidg ")
    processtime()
    wind.styler.combo.setCurrentText("Yohobaazul")
    wind.styler.combo.validator().fixup("Yohobaazul")
    processtime()
    wind.styler.combo.setCurrentText("QCheckBox")
    processtime()
    wind.styler.control_combo.setCurrentText("indicator")
    processtime()
    wind.styler.state_combo.setCurrentText("unchecked")
    processtime()
    wind.styler.table.cellWidget(0, 0).setCurrentText("border")
    processtime()
    wind.styler.table.item(0, 1).setText("3px solid #080")
    processtime()
    wind.styler.combo.validator().validate("")
    assert wind.styler.getWidgetState() == "QCheckBox:indicator::unchecked"


def test_style_manager(app, wind):
    """Test the style manager class object."""
    _, _ = app, wind
    manager = StyleManager()
    name, theme = next(iter(manager.themes.items()))
    for key, value in theme.items():
        manager.sheets.append({key: value})
    sheet = manager.get_sheet("QPushButton")
    assert sheet
    assert name
    assert app == manager.app
    assert get_manager()
