from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


def settings(self):
    # init translations
    start_up_lang = self.translations["prompts"]["startup_lang"]
    start_up_encrypt = self.translations["prompts"]["default_encrypt"]
    dark_mode = self.translations["prompts"]["dark_mode"]
    generate_keys = self.translations["prompts"]["generate_keys"]

    self.main_layout = QGridLayout()  # init layout
    title_label = QLabel("Settings")

    title_label.setAlignment(Qt.AlignCenter)
    title_label.setObjectName("title_label")
    title_label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed))
    title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    self.main_layout.addWidget(title_label, 0, 1, 1, 8)
    
    pad = QLabel(" ")
    self.main_layout.addWidget(pad, 0, 0, 1, 2)
    self.main_layout.addWidget(pad, 0, 8, 1, 2)

    # LANGUAGE SELECTION MENU
    self.button_lang = QPushButton(start_up_lang, self)
    menu = QMenu(self)
    menu.addAction("English")
    menu.addSeparator()
    menu.addAction("Suomi")
    menu.addSeparator()
    menu.addAction("Svenska")
    menu.setObjectName("lang_menu")
    self.button_lang.setMenu(menu)
    menu.triggered.connect(self.button_language)
    self.main_layout.addWidget(self.button_lang, 2, 2, 1, 6)

    # DEFAULT ENCRYPTION BUTTON
    self.button_default_crypt = QPushButton(start_up_encrypt, self)
    self.main_layout.addWidget(self.button_default_crypt, 4, 2, 1, 6)
    self.button_default_crypt.clicked.connect(self.default_encrypt_window)

    # GENERATE RSA KEYPAIR
    self.button_generate_keys = QPushButton(generate_keys, self)
    self.button_generate_keys.pressed.connect(self.generate_rsa_keys)
    self.main_layout.addWidget(self.button_generate_keys)

    # DARK MODE MENU
    self.button_dark_mode = QPushButton(dark_mode, self)
    self.button_dark_mode.pressed.connect(self.dark_mode_switch)
    self.main_layout.addWidget(self.button_dark_mode, 6, 2, 1, 6)

    # finish layout
    main = QWidget()
    main.setLayout(self.main_layout)
    return main
