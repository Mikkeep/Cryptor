"""Cryptor is a program made to handle encryption and
    decryption of files."""

import sys
import json
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from constants import *
from utils import *
from pages import settings, encryption, decryption, settings_page
from crypto import generate_key, encrypt


__author__ = "Mikael Pennanen & Juho Bruun"
__version__ = "1.0"
__name__ = "Cryptor"


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.w = None

        self.mdi = QMdiArea()

        # init lang from db
        CURRENT_LANG = read_used_lang(db_location)
        self.translations = self.read_translation(CURRENT_LANG)

        # set the title and icon of main window
        self.setWindowTitle(f"{__name__} v.{__version__}")
        self.setWindowIcon(QtGui.QIcon(IMG_LOCATION + "win_icon.png"))

        # set the size of window
        self.Width = 1200
        self.height = int(0.6 * self.Width)
        self.setFixedSize(self.Width, self.height)

        # center the window relative to screensize
        self.center_window()

        # init tab buttons
        self.btn_1 = QPushButton("", self)
        self.btn_1.setObjectName("encrypt_tab_btn")
        self.btn_2 = QPushButton("", self)
        self.btn_2.setObjectName("decrypt_tab_btn")
        self.btn_3 = QPushButton("", self)
        self.btn_3.setObjectName("settings_tab_btn")

        self.btn_1.setFixedSize(QtCore.QSize(180, 226))
        self.btn_1.clicked.connect(self.button1) 
        self.btn_2.setFixedSize(QtCore.QSize(180, 226))
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.setFixedSize(QtCore.QSize(180, 226))
        self.btn_3.clicked.connect(self.button3)


        # add tabs
        self._encryption = encryption.Encrypt_page(self.translations, self)
        self._decryption = decryption.Decrypt_page(self.translations)
        self.tab1 = self._encryption.encryption()
        self.tab2 = self._decryption.decryption()
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
        #left_layout.setObjectName("leftlayout")
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
        left_layout.addStretch(10)
        left_layout.setSpacing(0)
        left_layout.setContentsMargins(6, 10, 0, 0)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

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

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(left_widget)
        self.main_layout.addWidget(self.right_widget)
        self.main_layout.addWidget(self.right_layout)
        self.main_layout.setStretch(0, 40)
        self.main_layout.setStretch(1, 200)
        self.main_layout.setStretch(2, 40)
        main_widget = QWidget()
        main_widget.setLayout(self.main_layout)
        self.setCentralWidget(main_widget)

    def button1(self):
        self.right_widget.setCurrentIndex(0)

    def button2(self):
        self.right_widget.setCurrentIndex(1)

    def button3(self):
        self.right_widget.setCurrentIndex(2)

    def button_dec_t(self):
        self._decryption.button_dec_t()

    def button_dec_f(self):
        self._decryption.button_dec_f()

    def button_enc_t(self):
        self._encryption.button_enc_t()

    def button_enc_f(self):
        self._encryption.button_enc_f()

    def button_language(self, language):
        start_up_lang_info = self.translations["prompts"]["language_selection_info"]
        print(language.text())
        write_used_lang(db_location, (language.text(),))
        msg = QMessageBox()
        msg.setText(start_up_lang_info)
        display = msg.exec_()
        return language

    def dark_mode_switch(self):
        mode = check_dark_mode(db_location)
        print(mode)
        if mode == "False":
            write_used_mode(db_location, ("True",))
            with open("darkstyle.qss", "r") as f:
                _style = f.read()
                cryptor.setStyleSheet(_style)
            return
        else:
            write_used_mode(db_location, ("False",))
            with open("style.qss", "r") as f:
                _style = f.read()
                cryptor.setStyleSheet(_style)
            return

    def generate_rsa_keys(self):
        try:
            # Read both for confirmation they exist
            encrypt.Encryption().read_file("public.pem")
            encrypt.Encryption().read_file("private.pem")
            print("Found existing RSA key pair")
            keys_exist = self.translations["prompts"]["keys_exist"]
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(keys_exist)
            msg.exec_()
            return

        # If not found handle the error by generating new AES key pair
        except FileNotFoundError:

            print("Existing RSA key pair not found")

            generator = generate_key.key_generator()
            generator.generate_public_key()
            generator.generate_private_key()
            print("Generated public and private key pair for RSA encryption")
            keys_generated = self.translations["prompts"]["keys_generated"]
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(keys_generated)
            msg.exec_()
            return

    def default_encrypt_window(self):
        if self.w is None:
            self.w = settings.SettingsWindow(self.translations)
        self.w.show()

    def close_subwindow(self):
        self.mdi.close()


check_db(db_location)
defs = check_encryption_defaults(db_location)
print(defs)

cryptor = QApplication(sys.argv)

used_mode = check_dark_mode(db_location)
print("Darkmode state: ", used_mode)

if used_mode == "False":
    with open("style.qss", "r") as f:
        _style = f.read()
        cryptor.setStyleSheet(_style)

else:
    with open("darkstyle.qss", "r") as f:
        _style = f.read()
        cryptor.setStyleSheet(_style)

mainframe = Window()
mainframe.show()

sys.exit(cryptor.exec_())
