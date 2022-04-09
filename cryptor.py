#!/usr/bin/env python3

"""Cryptor is a program made to handle encryption and
    decryption of files."""


import sys
import json
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from constants import *
from utils import *


__author__ = "Mikael Pennanen & Juho Bruun"
__version__ = "1.0"
__name__ = "Cryptor"


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

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
        self.btn_1.setIcon(QtGui.QIcon("images/crypt.png"))
        self.btn_1.setIconSize(QtCore.QSize(100, 150))
        self.btn_2.clicked.connect(self.button2)
        self.btn_2.setIcon(QtGui.QIcon("images/key.png"))
        self.btn_2.setIconSize(QtCore.QSize(100, 150))
        self.btn_3.clicked.connect(self.button3)
        self.btn_3.setIcon(QtGui.QIcon("images/settings.png"))
        self.btn_3.setIconSize(QtCore.QSize(100, 150))

        # add tabs
        self.tab1 = self.encryption()
        self.tab2 = self.decryption()
        self.tab3 = self.settings()

        self.initUI()

    def read_translation(self, current_lang):
        translation = open("languages/" + current_lang, "r")
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

    def button_enc_t(self):
        self.bottom_widget.setCurrentIndex(0)

    def button_enc_f(self):
        self.bottom_widget.setCurrentIndex(1)

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

    def encryption(self):
        final_layout = QVBoxLayout()

        enc_button_text = self.translations["buttons"]["encrypt_text"]
        enc_button_files = self.translations["buttons"]["encrypt_files"]

        # add all widgets
        self.btn_enc_t = QPushButton(f"{enc_button_text}", self)
        self.btn_enc_t.clicked.connect(self.button_enc_t)
        self.btn_enc_f = QPushButton(f"{enc_button_files}", self)
        self.btn_enc_f.clicked.connect(self.button_enc_f)

        self.tab_enc_t = self.tab_enc_text()
        self.tab_enc_f = self.tab_enc_files()

        top_actions = QHBoxLayout()
        top_actions.addWidget(self.btn_enc_t)
        top_actions.addWidget(self.btn_enc_f)
        self.top_widget = QWidget()
        self.top_widget.setLayout(top_actions)

        self.bottom_widget = QTabWidget()
        self.bottom_widget.tabBar().setObjectName("EncryptionTab")

        self.bottom_widget.addTab(self.tab_enc_t, "")
        self.bottom_widget.addTab(self.tab_enc_f, "")

        self.bottom_widget.setCurrentIndex(0)

        final_layout.addWidget(self.top_widget)
        final_layout.addWidget(self.bottom_widget)

        main = QWidget()
        main.setLayout(final_layout)

        return main

    def decryption(self):

        final_layout = QVBoxLayout()

        dec_button_text = self.translations["buttons"]["decrypt_text"]
        dec_button_files = self.translations["buttons"]["decrypt_files"]

        self.btn_dec_t = QPushButton(f"{dec_button_text}", self)
        self.btn_dec_t.clicked.connect(self.button_dec_t)
        self.btn_dec_f = QPushButton(f"{dec_button_files}", self)
        self.btn_dec_f.clicked.connect(self.button_dec_f)

        self.tab_dec_t = self.tab_dec_text()
        self.tab_dec_f = self.tab_dec_files()

        top_actions = QHBoxLayout()
        top_actions.addWidget(self.btn_dec_t)
        top_actions.addWidget(self.btn_dec_f)
        self.top_widget_dec = QWidget()
        self.top_widget_dec.setLayout(top_actions)

        self.bottom_widget_dec = QTabWidget()
        self.bottom_widget_dec.tabBar().setObjectName("DecryptionTab")

        self.bottom_widget_dec.addTab(self.tab_dec_t, "")
        self.bottom_widget_dec.addTab(self.tab_dec_f, "")

        self.bottom_widget_dec.setCurrentIndex(0)

        final_layout.addWidget(self.top_widget_dec)
        final_layout.addWidget(self.bottom_widget_dec)

        main = QWidget()
        main.setLayout(final_layout)

        return main

    def settings(self):
        start_up_lang = self.translations["prompts"]["startup_lang"]
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(QLabel(start_up_lang))
        self.lang_list = QComboBox()
        self.lang_list.addItem("English")
        self.lang_list.addItem("Suomi")
        self.lang_list.addItem("Svenska")
        self.lang_list.currentIndexChanged.connect(self.button_choose_lang)
        self.main_layout.addWidget(self.lang_list)
        self.main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(self.main_layout)
        return main

    def tab_enc_text(self):
        bottom_layout = QVBoxLayout()
        bottom_layout.addWidget(QLabel(":)"))
        bottom_layout.addStretch(5)
        main = QWidget()
        main.setLayout(bottom_layout)
        return main

    def tab_enc_files(self):
        bottom_actions = QVBoxLayout()
        bottom_actions.addWidget(QLabel("(:"))
        bottom_actions.addStretch(5)
        main = QWidget()
        main.setLayout(bottom_actions)
        return main

    def tab_dec_text(self):
        bottom_layout = QVBoxLayout()
        bottom_layout.addWidget(QLabel(":)"))
        bottom_layout.addStretch(5)
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