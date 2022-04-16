from PyQt5.QtWidgets import *


def settings(self):
    # init translations
    start_up_lang = self.translations["prompts"]["startup_lang"]
    start_up_encrypt = self.translations["prompts"]["default_encrypt"]
    dark_mode = self.translations["prompts"]["dark_mode"]

    self.main_layout = QVBoxLayout() # init layout

    # LANGUAGE SELECTION MENU
    self.button_lang = QPushButton(start_up_lang, self)
    menu = QMenu(self)
    menu.addAction("English")
    menu.addSeparator()
    menu.addAction("Suomi")
    menu.addSeparator()
    menu.addAction("Svenska")
    self.button_lang.setMenu(menu)
    menu.triggered.connect(self.button_language)
    self.main_layout.addWidget(self.button_lang)

    # DEFAULT ENCRYPTION BUTTON
    self.button_default_crypt = QPushButton(start_up_encrypt, self)
    self.main_layout.addWidget(self.button_default_crypt)
    self.button_default_crypt.clicked.connect(self.default_encrypt_window)

    # DARK MODE MENU
    self.button_dark_mode = QPushButton(dark_mode, self)
    self.button_dark_mode.pressed.connect(self.dark_mode_switch)
    self.main_layout.addWidget(self.button_dark_mode)

    # finish layout
    main = QWidget()
    main.setLayout(self.main_layout)
    return main
