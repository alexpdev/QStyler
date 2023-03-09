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
import re
import sys
import time

import pytest
from PySide6.QtWidgets import QApplication, QMainWindow

from QStyler import __main__, version
from QStyler.dialog import NewDialog, RenameDialog
from QStyler.utils import QssParser
from QStyler.window import Application


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
    # app.window.show()  # only for testing locally
    yield app.window
    app.window.close()
    app.window.deleteLater()


def processtime(app=None, amount=None):
    """Process Events and sleep for a second."""
    app = app if app else QApplication.instance()
    if not amount:
        amount = 0.01
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


def test_menu_bar(wind):
    """
    Test the menu bar.

    Parameters
    ----------
    pre: tuple
        the app and window.
    """
    assert wind.menuBar()


def test_parser():
    """Test qss parser class."""
    parent = os.path.dirname(__file__)
    filepath = os.path.join(parent, "test.qss")
    content = open(filepath, "rt", encoding="utf8").read()
    parser = QssParser(content)
    assert parser.results


def test_tickers(wind):
    """Test the tickers in slider widgets."""
    wind.tabWidget.setCurrentIndex(1)
    processtime()
    tab = wind.widgets
    while tab.verticalSlider.value() < 99:
        tab.verticalSlider.triggerAction(
            tab.verticalSlider.SliderAction.SliderSingleStepAdd
        )
        tab.horizontalSlider.triggerAction(
            tab.horizontalSlider.SliderAction.SliderSingleStepAdd
        )
        processtime(amount=0.02)
    assert tab.verticalSlider.value() > 95
    assert tab.horizontalSlider.value() > 95


def test_toolbar_apply_osx(app, wind):
    """Test applying osx theme to application."""
    wind.tabWidget.setCurrentIndex(1)
    processtime(app=app)
    toolbar = wind.styler.toolbar
    toolbar.themes_combo.setCurrentText("OSX")
    toolbar.live_action.trigger()
    toolbar.load_action.trigger()
    toolbar.live_action.trigger()
    wind.tabWidget.setCurrentIndex(1)
    assert "OSX" == toolbar.themes_combo.currentText()


def test_toolbar_reset_theme(app, wind):
    """Test applying reseting theme to application."""
    wind.tabWidget.setCurrentIndex(1)
    processtime(app=app)
    toolbar = wind.styler.toolbar
    toolbar.themes_combo.setCurrentIndex(0)
    toolbar.live_action.trigger()
    toolbar.load_action.trigger()
    toolbar.reset_action.trigger()
    toolbar.load_action.trigger()
    assert toolbar.themes_combo.currentText()


def test_new_dialog(app):
    """Test new dialog."""
    dialog = NewDialog("name")
    processtime(app)
    dialog.save()


def test_rename_dialog(app):
    """Test rename dialog."""
    dialog = RenameDialog("name")
    processtime(app)
    dialog.save()


@pytest.mark.parametrize(
    "theme", ["OSX", "KnightRider", "Overcaset", "Terminal", "Bland"]
)
def test_toolbar_buttons(app, wind, theme):
    """Test function for toolbar buttons."""
    wind.tabWidget.setCurrentIndex(0)
    processtime(app=app)
    toolbar = wind.styler.toolbar
    toolbar.live_action.toggle()
    for i in range(toolbar.themes_combo.count()):
        if toolbar.themes_combo.itemText(i) == theme:
            toolbar.themes_combo.setCurrentIndex(i)
            processtime(app)
            break
    processtime(app)
    toolbar.preview_action.trigger()
    processtime(app)
    toolbar.preview_action.trigger()
    processtime(app)
    toolbar.load_action.trigger()
    processtime(app)
    toolbar.live_action.toggle()
    processtime(app)
    toolbar.reset_action.trigger()
    processtime(app)
    wind.tabWidget.setCurrentIndex(1)
    assert wind.styler.editor.toPlainText() == ""


@pytest.mark.parametrize(
    "theme", ["SummerBreeze", "MaterialDarkStyle", "DarkSkyline", "Coastal"]
)
def test_styler_with_theme(app, wind, theme):
    """Test function for toolbar buttons."""
    wind.tabWidget.setCurrentIndex(0)
    processtime(app=app, amount=0.1)
    styler = wind.styler
    toolbar = styler.toolbar
    themes = toolbar.themes_combo
    for i in range(themes.count()):
        if themes.itemText(i) == theme:
            themes.setCurrentIndex(i)
            processtime(app)
            break
    for i in range(styler.widget_list.count()):
        item = styler.widget_list.item(i)
        styler.on_widget_clicked(item)
        styler.on_widget_double_clicked(item)

        processtime(app)
    styler.editor.clear()
    processtime(app)
    assert themes.currentText() == theme


def test_color_picker(wind, app):
    """Test styler color picker."""
    wind.tabWidget.setCurrentIndex(0)
    processtime(app=app, amount=0.0001)
    styler = wind.styler
    picker = styler.colorPicker
    styler.editor.clear()
    for slider in [picker.red_slider, picker.blue_slider]:
        for value in range(2, 200):
            slider.setValue(value)
            processtime(app=app, amount=0.00001)
    styler.toolbar.reset_action.trigger()
    styler.toolbar.themes_combo.setCurrentIndex(5)
    processtime(app=app, amount=0.1)
    text = styler.editor.toPlainText()
    processtime(app=app, amount=0.1)
    match = re.search(r"\s#\w+?;", text)
    pos = match.end()
    cursor = styler.editor.textCursor()
    cursor.setPosition(pos, cursor.MoveMode.MoveAnchor)
    styler.editor.setTextCursor(cursor)
    for i in range(20):
        picker.red_slider.setValue(i)
        processtime(app=app, amount=0.1)
    styler.editor.clear()
    assert styler.editor.toPlainText() == ""


def test_save_theme(wind, app):
    """Test save action button."""
    wind.tabWidget.setCurrentIndex(0)
    processtime(app=app, amount=0.2)
    styler = wind.styler
    styler.toolbar.themes_combo.setCurrentIndex(4)
    styler.toolbar.save_action.trigger()
    styler.toolbar.reset_action.trigger()
    assert styler.editor.toPlainText() == ""


def test_new_delete_theme(app, wind):
    """Test new theme and delete theme actions."""
    wind.tabWidget.setCurrentIndex(0)
    toolbar = wind.styler.toolbar
    processtime(app=app)
    toolbar.new_action.trigger()
    processtime(app=app)
    toolbar.dialog.line.setText("new_test_theme")
    processtime(app=app)
    toolbar.dialog.save_btn.click()
    processtime(app=app)
    combo = toolbar.themes_combo
    processtime(app=app)
    for i in range(combo.count()):
        if combo.itemText(i) == "new_test_theme":
            combo.setCurrentIndex(i)
            break
    toolbar.rename_action.trigger()
    processtime(app=app)
    toolbar.dialog.line.setText("new_new_test_theme")
    processtime(app=app)
    toolbar.dialog.save_btn.click()
    processtime(app=app)
    assert toolbar.themes_combo.currentText() == "new_new_test_theme"
    toolbar.delete_action.trigger()
    processtime(app=app)
    assert toolbar.themes_combo.currentText() != "new_new_test_theme"


def test_extend_button(wind, app):
    """Test the extend button functionality."""
    wind.tabWidget.setCurrentIndex(0)
    toolbar = wind.styler.toolbar
    processtime(app=app)
    toolbar.extend_action.trigger()
    processtime(app=app)
    assert toolbar.extended_state is True
    toolbar.extend_action.trigger()
    processtime(app=app)
    assert toolbar.extended_state is False


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
            os.remove(test_json)  # pragma: nocover
