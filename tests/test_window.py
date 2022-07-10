import os
import sys
import pytest

from PySide6.QtWidgets import QApplication

from QStyler.window import MainWindow


@pytest.fixture
def app():
    app = QApplication(sys.argv)


def test_main_window(app):
    mainwindow = MainWindow()
    mainwindow.show()
    assert mainwindow
