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

    def _initMain(self):
        self.setWindowTitle(f"{__name__} v.{__version__}")
        self.setGeometry(235, 235, 300, 260)
        self._centralWidget = QWidget(self)
        self.show()

cryptor= QApplication(sys.argv)
mainframe = Mainframe()
sys.exit(cryptor.exec_())