from PyQt5.QtWidgets import *


def settings(self):
    start_up_lang = self.translations["prompts"]["startup_lang"]
    start_up_encrypt = self.translations["prompts"]["default_encrypt"]
    dark_mode = self.translations["prompts"]["dark_mode"]
    self.main_layout = QVBoxLayout()
    self.button_lang = QPushButton(start_up_lang, self)
    menu = QMenu(self)
    menu.addAction("English")
    menu.addSeparator()
    menu.addAction("Suomi")
    menu.addSeparator()
    menu.addAction("Svenska")
    menu.setStyleSheet('width: 754px;')
    self.button_lang.setMenu(menu)
    menu.triggered.connect(self.button_language)
    self.main_layout.addWidget(self.button_lang)
    self.button_default_crypt = QPushButton(start_up_encrypt, self)
    self.main_layout.addWidget(self.button_default_crypt)
    self.button_default_crypt.clicked.connect(self.default_encrypt_window)
    self.button_dark_mode = QPushButton(dark_mode, self)
    darkmode_menu = QMenu(self)
    darkmode_menu.addAction("On")
    darkmode_menu.addSeparator()
    darkmode_menu.addAction("Off")
    darkmode_menu.setStyleSheet('width: 754px;')
    self.button_dark_mode.setMenu(darkmode_menu)
    darkmode_menu.triggered.connect(self.dark_mode_switch)
    self.main_layout.addWidget(self.button_dark_mode)
    main = QWidget()
    main.setLayout(self.main_layout)
    return main
