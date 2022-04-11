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


__author__ = "Mikael Pennanen & Juho Bruun"
__version__ = "1.0"
__name__ = "Cryptor"

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.chosen_algo = ""
        self.chosen_salt = ""
        self.chosen_key = ""
        self.settings_translate = Window().translations
        enc_key = self.settings_translate["buttons"]["encryption_key_prompt"]
        enc_key_confirm = self.settings_translate["buttons"]["encryption_key_confirm"]
        algorithm = self.settings_translate["buttons"]["algorithm"]
        salt = self.settings_translate["buttons"]["salt"]
        close_btn = self.settings_translate["prompts"]["close_button"]

        self.algorithm = QPushButton(algorithm)
        self.text_box_salt = PasswordEdit(self)
        self.text_box_salt.setPlaceholderText(salt)
        self.text_box_enc_text = PasswordEdit(self)
        self.text_box_enc_text.setPlaceholderText(enc_key)
        self.text_box_enc_text_confirm = PasswordEdit(self)
        self.text_box_enc_text_confirm.setPlaceholderText(enc_key_confirm)
        self.close_button = QPushButton(close_btn)
        self.close_button.clicked.connect(self.close_settings)
        self.menu = QMenu(self)
        self.menu.addAction('MD5')
        self.menu.addSeparator()
        self.menu.addAction('SHA-256')
        self.menu.addSeparator()
        self.menu.addAction('SHA-512')
        self.menu.addSeparator()
        self.menu.addAction('SHA3-512')
        self.algorithm.setMenu(self.menu)
        self.menu.triggered.connect(self.algorithms)
        layout.addWidget(self.algorithm)
#        layout.addWidget(self.salt)
        layout.addWidget(self.text_box_salt)
        layout.addWidget(self.text_box_enc_text)
        layout.addWidget(self.text_box_enc_text_confirm)
        layout.addSpacing(50)
        layout.addWidget(self.close_button)
        self.setLayout(layout)

        self.Width = 570
        self.height = int(0.6 * self.Width)
        self.setFixedSize(self.Width, self.height)
        # center the window relative to screensize
        centering = self.frameGeometry()
        centerOfScreen = QDesktopWidget().availableGeometry().center()
        centering.moveCenter(centerOfScreen)
        self.move(centering.topLeft())


    def algorithms(self, language):
        self.chosen_algo = language.text()
        print(language.text())
        return language

    def close_settings(self, event):
        pwd_mismatch = self.settings_translate["prompts"]["password_mismatch"]
        confirm_no_enc_key_set = self.settings_translate["prompts"]["confirm_no_password"]
        no_enc_key_prompt = self.settings_translate["prompts"]["no_enc_key"]
        print("Chosen algorithm: ", self.chosen_algo)
        print("Chosen salt: ", self.text_box_salt.text())
        print("Chosen enc key: ", self.text_box_enc_text.text())
        print("Chosen enc key: ", self.text_box_enc_text_confirm.text())
        if self.text_box_enc_text.text() == self.text_box_enc_text_confirm.text():
            if str(self.text_box_enc_text.text()) == "" and str(self.text_box_enc_text_confirm.text()) == "":
                confirm_no_pwd = QMessageBox.question(self, no_enc_key_prompt, confirm_no_enc_key_set, QMessageBox.Yes | QMessageBox.No)
                if confirm_no_pwd == QMessageBox.Yes:
                    self.close()
                    print("Default values saved succesfully")
                    return
                return
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(pwd_mismatch)
            display = msg.exec_()
            return

        self.close()

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
        self.tab1 = self.encryption()
        self.tab2 = self.decryption()
        self.tab3 = self.settings()

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
            self.w = SettingsWindow()
        self.w.show()
        self.sub = QMdiSubWindow()
#        self.sub.setWidget(QTextEdit("MOI"))
        self.sub.setWindowTitle("subwindow")
        self.mdi.addSubWindow(self.sub)
        self.sub.show()

    def close_subwindow(self):
        self.mdi.close()

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
        start_up_encrypt = self.translations["prompts"]["default_encrypt"]
        dark_mode = self.translations["prompts"]["dark_mode"]
        self.main_layout = QVBoxLayout()
#        self.main_layout.addWidget(QLabel(start_up_lang))
        self.button_lang = QPushButton(start_up_lang, self)
        menu = QMenu(self)
        menu.addAction('English')
        menu.addSeparator()
        menu.addAction('Suomi')
        menu.addSeparator()
        menu.addAction('Svenska')
        self.button_lang.setMenu(menu)
        menu.triggered.connect(self.button_language)
        self.main_layout.addWidget(self.button_lang)
#        self.lang_list = QComboBox()
#        self.lang_list.addItem("English")
#        self.lang_list.addItem("Suomi")
#        self.lang_list.addItem("Svenska")
#        self.lang_list.currentIndexChanged.connect(self.button_choose_lang)
#        self.main_layout.addWidget(self.lang_list)
#        self.main_layout.addStretch(5)
#        self.main_layout.addWidget(QLabel(start_up_encrypt))
        self.button_default_crypt = QPushButton(start_up_encrypt, self)
        self.main_layout.addWidget(self.button_default_crypt)
        self.button_default_crypt.clicked.connect(self.default_encrypt_window)
        self.button_dark_mode = QPushButton(dark_mode, self)
        self.main_layout.addWidget(self.button_dark_mode)
        main = QWidget()
        main.setLayout(self.main_layout)
        return main

    def tab_enc_text(self):
        self.bottom_layout = QVBoxLayout()
        self.leiska2 = QVBoxLayout()
        self.bottom_layout.setContentsMargins(0,0,0,0)
        self.bottom_layout.setSpacing(0)
#        bottom_layout.addStretch(5)
        widget = QLabel("Hello")
        font = widget.font()
        font.setPointSize(10)
        widget.setFont(font)
        self.text_box_enc_text = PasswordEdit(self)
        self.text_box_enc_text_confirm = PasswordEdit(self)
        label_1 = QLabel()
        label_1.setText("Encryption here: ")
        self.bottom_layout.addWidget(widget)
        self.bottom_layout.addWidget(self.text_box_enc_text)
        LOL = self.bottom_layout.addWidget(self.text_box_enc_text_confirm)
        main = QWidget()
        main.setLayout(self.bottom_layout)
        return main

    def tab_enc_files(self):
        bottom_actions = QVBoxLayout()
        bottom_actions.addWidget(QLabel("(:"))
#        bottom_actions.addStretch(5)
        main = QWidget()
        main.setLayout(bottom_actions)
        return main

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
