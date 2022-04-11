#!/usr/bin/env python3

"""Cryptor is a program made to handle encryption and
    decryption of files."""


from cProfile import label
import sys
import json
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore, Qt, QtWidgets
from qtwidgets import PasswordEdit
from constants import *
from utils import *
from pages import settings, encryption, decryption, settings_page

__author__ = "Mikael Pennanen & Juho Bruun"
__version__ = "1.0"
__name__ = "Cryptor"


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.w = None

        self.mdi = QMdiArea()

        CURRENT_LANG = read_used_lang(db_location)
        self.translations = self.read_translation(CURRENT_LANG)

        # set the title of main window
        self.setWindowTitle(f"{__name__} v.{__version__}")

        # set the size of window
        self.Width = 830
        self.height = int(0.6 * self.Width)
        self.setFixedSize(self.Width, self.height)
        # center the window relative to screensize
        self.center_window()

        # add all widgets

        self.btn_1 = QPushButton("", self)
        self.btn_2 = QPushButton("", self)
        self.btn_3 = QPushButton("", self)

        self.btn_1.clicked.connect(self.button1)
        self.btn_1.setIcon(QtGui.QIcon(IMG_LOCATION + "crypt.png"))
        self.btn_1.setIconSize(QtCore.QSize(100, 150))
        self.btn_2.clicked.connect(self.button2)
        self.btn_2.setIcon(QtGui.QIcon(IMG_LOCATION + "key.png"))
        self.btn_2.setIconSize(QtCore.QSize(100, 150))
        self.btn_3.clicked.connect(self.button3)
        self.btn_3.setIcon(QtGui.QIcon(IMG_LOCATION + "settings.png"))
        self.btn_3.setIconSize(QtCore.QSize(100, 150))

        # add tabs
        _encryption = encryption.Encrypt_page(self.translations)
        self.tab1 = _encryption.encryption()
        self.tab2 = decryption.decryption(self)
        self.tab3 = settings_page.settings(self)

        self.initUI()

    def read_translation(self, current_lang):
        translation = open(LANG_LOCATION + current_lang, "r")
        words = json.loads(translation.read())
        return words

    def center_window(self):
        centering = self.frameGeometry()
        centerOfScreen = QDesktopWidget().availableGeometry().center()
        centering.moveCenter(centerOfScreen)
        self.move(centering.topLeft())

    def initUI(self):
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
        left_layout.addStretch(10)
        left_layout.setSpacing(0)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        left_widget.setStyleSheet(
            #                        "background-color: grey;"
            #                        "selection-color: grey;"
            #                        "selection-background-color: grey;"
            "padding-top: 0px;"
            "padding-bottom: 0px;"
        )

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, "")
        self.right_widget.addTab(self.tab2, "")
        self.right_widget.addTab(self.tab3, "")

        self.right_widget.setCurrentIndex(0)

        self.right_layout = QListWidget()
        progress = self.translations["prompts"]["in_progress"]
        self.right_layout.addItems([f"{progress} ({len(inprogresslist)})"])
        self.right_layout.resize(200, self.height)

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.addWidget(self.right_layout)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_layout.setStretch(2, 40)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def button1(self):
        self.right_widget.setCurrentIndex(0)

    def button2(self):
        self.right_widget.setCurrentIndex(1)

    def button3(self):
        self.right_widget.setCurrentIndex(2)

    def button_dec_t(self):
        self.bottom_widget_dec.setCurrentIndex(0)

    def button_dec_f(self):
        self.bottom_widget_dec.setCurrentIndex(1)

    def button_choose_lang(self, language):
        start_up_lang_info = self.translations["prompts"]["language_selection_info"]
        self.translations = self.read_translation(self.lang_list.currentText())
        print(self.lang_list.currentText())
        write_used_lang(db_location, (self.lang_list.currentText(),))
        msg = QMessageBox()
        msg.setText(start_up_lang_info)
        display = msg.exec_()
        return language

    def button_language(self, language):
        start_up_lang_info = self.translations["prompts"]["language_selection_info"]
        print(language.text())
        write_used_lang(db_location, (language.text(),))
        msg = QMessageBox()
        msg.setText(start_up_lang_info)
        display = msg.exec_()
        return language

    def default_encrypt_window(self):

        if self.w is None:
            self.w = settings.SettingsWindow(self.translations)
        self.w.show()
        self.sub = QMdiSubWindow()
        self.sub.setWindowTitle("subwindow")
        self.mdi.addSubWindow(self.sub)
        self.sub.show()

    def close_subwindow(self):
        self.mdi.close()

    def tab_dec_text(self):
        bottom_layout = QVBoxLayout()
        bottom_layout.addWidget(QLabel(":)"))
        #        bottom_layout.addStretch(5)
        main = QWidget()
        main.setLayout(bottom_layout)
        return main

    def tab_dec_files(self):
        bottom_actions = QVBoxLayout()
        bottom_actions.addWidget(QLabel("(:"))
        bottom_actions.addStretch(5)
        main = QWidget()
        main.setLayout(bottom_actions)
        return main


check_db(db_location)

cryptor = QApplication(sys.argv)

mainframe = Window()
mainframe.show()

with open("style.qss", "r") as f:
    _style = f.read()
    cryptor.setStyleSheet(_style)

sys.exit(cryptor.exec_())
