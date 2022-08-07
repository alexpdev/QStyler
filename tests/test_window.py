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

import atexit
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
    # window.show() # only for testing locally
    yield window
    window.close()
    window.deleteLater()


def processtime(app=None, amount=None):
    """Process Events and sleep for a second."""
    app = app if app else QApplication.instance()
    if not amount:
        amount = 0.03
    start = time.time()
    while time.time() - start < amount:
        app.processEvents()


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
    assert wind.menuBar()


def test_plus_button(wind):
    """
    Test the styler tab widget combo box.

    Parameters
    ----------
    window : tuple
        _description_
    """
    wind.tabWidget.setCurrentIndex(0)
    processtime()
    tab = wind.styler
    toolbar = tab.toolbar
    toolbar.plus_button_action.trigger()
    assert len(tab.boxgroups) > 0
    processtime()
    tab.combo.setCurrentIndex(5)
    processtime()
    toolbar.plus_button_action.trigger()
    assert len(tab.boxgroups) > 0
    processtime()
    toolbar.minus_button_action.trigger()
    processtime()
    assert len(tab.boxgroups) == 0


def test_apply_theme(wind):
    """
    Test applying theme.

    Parameters
    ----------
    window : tuple
        _description_
    """
    wind.tabWidget.setCurrentIndex(1)
    processtime()
    themeactions = wind.menubar.optionsMenu.themeMenu.actions()
    for action in themeactions:
        action.trigger()
        processtime()
        tab = wind.styler
        for i in range(tab.combo.count()):
            text = tab.combo.itemText(i)
            if text == "QPushButton":
                text = tab.combo.setCurrentIndex(i)
                break
        processtime()
    assert tab.table.rowCount() > 0


def test_set_property(wind):
    """
    Test applying theme.

    Parameters
    ----------
    window : QMainWindow
        The MainWindow instance
    """
    wind.tabWidget.setCurrentIndex(0)
    processtime()
    tab = wind.styler
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
    wind.tabWidget.setCurrentIndex(0)
    processtime()
    tab = wind.styler
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
    theme = next(iter(wind.menubar.optionsMenu.themeactions))
    theme.trigger()
    processtime()
    for i in range(tab.combo.count()):
        text = tab.combo.itemText(i)
        if text == "QSpinBox":
            break
    processtime()
    text = tab.combo.setCurrentIndex(i)
    wind.menubar.optionsMenu.resetAction.trigger()
    processtime()
    assert tab.table.rowCount() > 1


def test_style_table_props(wind, app):
    """Test the props combos in the style table."""
    actions = wind.menubar.optionsMenu.themeactions
    wind.tabWidget.setCurrentIndex(1)
    processtime(app)
    first_theme = next(iter(actions))
    first_theme.trigger()
    processtime(app)
    styler = wind.styler
    styler.combo.setCurrentText("QLineEdit")
    processtime(app)
    wind.tabWidget.setCurrentIndex(0)
    processtime(app)
    styler.table.cellWidget(0, 0).setCurrentText("color")
    styler.table.item(0, 1).setText("#F00")
    processtime(app)
    assert "color: #F00;" in app.styleSheet()


def test_tickers(wind):
    """Test the tickers in slider widgets."""
    wind.tabWidget.setCurrentIndex(1)
    processtime()
    tab = wind.widgets
    while tab.verticalSlider.value() < 99:
        tab.verticalSlider.triggerAction(
            tab.verticalSlider.SliderSingleStepAdd
        )
        tab.horizontalSlider.triggerAction(
            tab.horizontalSlider.SliderSingleStepAdd
        )
        processtime(amount=0.02)
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
    out = manager.result
    assert len(out) == 7


def test_validator_combo(wind):
    """Test the combo validator."""
    wind.tabWidget.setCurrentIndex(0)
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
    wind.tabWidget.setCurrentIndex(0)
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


def test_style_manager(wind, app):
    """Test the style manager class object."""
    wind.tabWidget.setCurrentIndex(1)
    manager = StyleManager()
    title = manager.titles[3]
    theme = manager.get_theme(title)
    for key, value in theme.items():
        manager.sheets.append({key: value})
    sheet = manager.get_sheet("QPushButton")
    processtime()
    assert sheet
    assert title
    assert app == manager.app
    assert get_manager()


def test_add_new_theme(app, wind):
    """Testing adding a new theme."""
    wind.tabWidget.setCurrentIndex(1)
    processtime(app=app)
    parser = QssParser("tests/test.qss")
    thememenu = wind.menubar.optionsMenu
    thememenu.add_new_theme(parser.result, "test")
    keys = []
    for action in thememenu.themeactions:
        keys.append(action.key)
    assert "test" in keys


def test_get_theme_file(wind):
    """Test getThemeFile method form the LoadAction object."""
    action = wind.menubar.loadAction
    wind.tabWidget.setCurrentIndex(1)
    processtime()
    action.getThemeFile("test", "tests/test.qss")
    titles = []
    for i in range(wind.styler.toolbar.themecombo.count()):
        text = wind.styler.toolbar.themecombo.itemText(i)
        titles.append(text)
    assert "test" in titles


def test_style_manager_get_sheet(wind):
    """Test the style managers get_sheet method."""
    wind.tabWidget.setCurrentIndex(1)
    manager = get_manager()
    manager.apply_theme("MintyMixup")
    widgets = [
        "QMainWindow",
        "QCalendar",
        "QPushButton",
        "QPushButton::default",
        "QMenuBar",
        "QMenu",
    ]
    text = ",".join(widgets)
    sheet = manager.get_sheet(text)
    assert "background-color" in sheet.keys()


def test_style_manager_get_sheet2(wind):
    """Test the style managers get_sheet2 method."""
    wind.tabWidget.setCurrentIndex(1)
    manager = get_manager()
    manager.apply_theme("MintyMixup")
    sheet = manager.get_sheet("")
    assert not sheet


def test_style_manager_get_sheet3(wind):
    """Test the style managers get_sheet3 method."""
    wind.tabWidget.setCurrentIndex(1)
    manager = get_manager()
    manager.apply_theme("MintyMixup")
    widgets = ["QMenu", "QLineEdit", "QLabel"]
    text = ",".join(widgets)
    sheet = manager.get_sheet(text)
    assert not sheet


def test_toolbar_apply_osx(app, wind):
    """Test applying osx theme to application."""
    wind.tabWidget.setCurrentIndex(1)
    processtime(app=app)
    toolbar = wind.styler.toolbar
    toolbar.themecombo.setCurrentText("OSX")
    toolbar.apply_theme_action.trigger()
    wind.tabWidget.setCurrentIndex(1)
    assert "OSX" == toolbar.themecombo.currentText()


def test_toolbar_reset_theme(app, wind):
    """Test applying reseting theme to application."""
    wind.tabWidget.setCurrentIndex(1)
    processtime(app=app)
    toolbar = wind.styler.toolbar
    toolbar.themecombo.setCurrentIndex(0)
    toolbar.apply_theme_action.trigger()
    assert not toolbar.themecombo.currentText()


def test_get_theme_styler_empty(wind):
    """Test get_theme method without proper theme title."""
    _ = wind
    manager = get_manager()
    theme = manager.get_theme("poptarts")
    assert not theme


def test_toolbar_plus_button(app, wind):
    """Test plus button."""
    toolbar = wind.styler.toolbar
    wind.tabWidget.setCurrentIndex(0)
    toolbar.reset_theme_action.trigger()
    processtime(app=app)
    wind.styler.combo.setCurrentIndex(0)
    processtime(app=app)
    toolbar.plus_button_action.trigger()
    processtime(app=app)
    assert len(wind.styler.boxgroups) == 1


def test_toolbar_minus_button(app, wind):
    """Test toolbar minus button."""
    wind.tabWidget.setCurrentIndex(0)
    processtime(app=app)
    toolbar = wind.styler.toolbar
    toolbar.minus_button_action.trigger()
    processtime(app=app)
    toolbar.minus_button_action.trigger()
    processtime(app=app)
    toolbar.minus_button_action.trigger()
    processtime(app=app)
    toolbar.minus_button_action.trigger()
    processtime(app=app)
    toolbar.minus_button_action.trigger()
    assert len(wind.styler.boxgroups) == 0


def test_update_table_props(wind):
    """
    Test table prop updates.
    """
    wind.tabWidget.setCurrentIndex(0)
    processtime()
    table = wind.styler.table
    combo = table.cellWidget(0, 0)
    combo.setCurrentIndex(5)
    processtime()
    table.widgetChanged.emit("changed")
    item = table.item(0, 1)
    item.setText("transparent")
    processtime()
    table.cellChanged.emit(0, 1)
    processtime()
    assert table.item(0, 1).text() == "transparent"


def test_update_prop(wind):
    """Test update prop method in the Table."""
    wind.tabWidget.setCurrentIndex(0)
    processtime()
    table = wind.styler.table
    toolbar = wind.styler.toolbar
    processtime()
    for i in range(toolbar.themecombo.count()):
        if toolbar.themecombo.itemText(i) == "Ubuntu":
            toolbar.themecombo.setCurrentIndex(i)
            processtime(amount=0.02)
            break
    toolbar.apply_theme_action.trigger()
    processtime()
    wind.styler.combo.setCurrentText("QPushButton")
    processtime()
    assert table.cellWidget(0, 0).currentText() != ""
    wind.styler.state_combo.setCurrentText("hover")
    processtime()
    assert table.cellWidget(0, 0).currentText() == ""


@atexit.register
def teardown():
    """
    Clean up any additional test residual artifacts.
    """
    fd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    theme_dir = os.path.join(fd, "QStyler", "themes")
    if os.path.exists(theme_dir):
        test_json = os.path.join(theme_dir, "test.json")
        if os.path.exists(test_json):
            os.remove(test_json)
