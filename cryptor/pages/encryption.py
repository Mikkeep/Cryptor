from PyQt5.QtWidgets import *
from qtwidgets import PasswordEdit

class Encrypt_page():

    def __init__(self, translations):
        self.translations = translations

    def button_enc_t(self):
        print("Painoit button enc t")
        self.bottom_widget.setCurrentIndex(0)

    def button_enc_f(self):
        print("Painoit button enc f")
        self.bottom_widget.setCurrentIndex(1)

    def encryption(self):
        final_layout = QVBoxLayout()

        enc_button_text = self.translations["buttons"]["encrypt_text"]
        enc_button_files = self.translations["buttons"]["encrypt_files"]

        # add all widgets
        self.btn_enc_t = QPushButton(f"{enc_button_text}")
        self.btn_enc_t.clicked.connect(self.button_enc_t)
        self.btn_enc_f = QPushButton(f"{enc_button_files}")
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

    def tab_enc_text(self):
        self.bottom_layout = QVBoxLayout()
        self.leiska2 = QVBoxLayout()
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setSpacing(0)
        self.text_box_enc_text = PasswordEdit(self)
        self.text_box_enc_text_confirm = PasswordEdit(self)
        label_1 = QLabel()
        label_1.setText("Encryption here: ")
#        self.bottom_layout.addWidget(widget)
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