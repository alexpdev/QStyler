import os
import sys
import pytest

from PySide6.QtWidgets import QApplication

from QStyler.window import MainWindow


@pytest.fixture(scope="module")
def app():
    app = QApplication(sys.argv)
    app.quit()
    del app


def test_main_window(app):
    mainwindow = MainWindow()
    mainwindow.show()
    assert mainwindow

def test_menu_bar(app):
    mainwindow = MainWindow()
    mainwindow.show()
    mainwindow.menubar.fileMenu.showStyles()
    assert mainwindow
