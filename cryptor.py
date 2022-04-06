#!/usr/bin/env python3

"""Cryptor is a program made to handle encryption and
    decryption of files."""


import sys

from PyQt5.QtWidgets import *

__author__ = "Mikael Pennanen & Juho Bruun"
__version__ = "1.0"
__name__ = "Cryptor"


class Mainframe(QMainWindow):
    #This is the main window of the application
    def __init__(self):
        super().__init__()

        self._initMain()
        self._createMenu()

    def _initMain(self):
        self.setWindowTitle(f"{__name__} v.{__version__}")
        self.setGeometry(235, 235, 300, 260)

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

app = QApplication([])
app.setApplicationName(f"{__name__}")
text = QPlainTextEdit()
window = Mainframe()
window.setCentralWidget(text)
window.show()
app.exec_()
