from PyQt5.QtWidgets import *
from qtwidgets import PasswordEdit
from .file_dialog import FileDialog
from constants import ENC_ALGORITHMS



class Encrypt_page:
    def __init__(self, translations):
        self.translations = translations

    def button_enc_t(self):
        self.bottom_widget.setCurrentIndex(0)

    def button_enc_f(self):
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
        layout = QGridLayout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 2)

        # INSERT TEXT BOX
        text_to_enc_label = QLabel()
        text_to_enc_label.setText("Insert text to encrypt:") 
        text_insert = QLineEdit()
        layout.addWidget(text_insert, 0, 1, 1, 3)
        layout.addWidget(text_to_enc_label, 0, 0)
        
        # ALGORITHM DROPDOWN MENU 
        algo_text_label = QLabel()
        algo_text_label.setText("Set encryption algorithm:")
        layout.addWidget(algo_text_label, 1, 0, 1, 1)
        algo_trans = self.translations["buttons"]["algorithm"]
        self.algo_button = QPushButton(algo_trans)
        self.algo_dropdown = QMenu()
        for algo in ENC_ALGORITHMS:
            self.algo_dropdown.addAction(algo)
            self.algo_dropdown.addSeparator()
        self.algo_button.setMenu(self.algo_dropdown)
        layout.addWidget(self.algo_button, 1, 1, 1, 3)

        # ENCRYPTION KEY INPUT AND CONFIRM 
        enc_text_label = QLabel("Set encryption key:")
        enc_conf_label = QLabel("Confirm key:")
        self.text_box_enc_text = PasswordEdit(self)
        self.text_box_enc_text_confirm = PasswordEdit(self)
        layout.addWidget(enc_text_label, 2, 0, 1, 1)
        layout.addWidget(self.text_box_enc_text, 2, 1)
        layout.addWidget(enc_conf_label, 2, 2)
        layout.addWidget(self.text_box_enc_text_confirm, 2, 3)

        # SALT INPUT
        salt_label = QLabel("Insert encryption salt:")
        self.salt_insert_box = PasswordEdit(self)
        layout.addWidget(salt_label, 3, 0, 1, 1)
        layout.addWidget(self.salt_insert_box, 3, 1, 1, 3)

        # ENCRYPT BUTTON
        enc_trans = self.translations["buttons"]["final_encrypt"]
        self.encrypt_button = QPushButton(enc_trans)
        layout.addWidget(self.encrypt_button, 4, 0, 1, 4)
        main = QWidget()
        main.setLayout(layout)
        return main

    def filedialogopen(self):
        self._files = FileDialog().fileOpen()

    def filedialogsave(self):
        self._save = FileDialog().fileSave()

    def tab_enc_files(self):
        bottom_actions = QVBoxLayout()

        # FILE BROWSE
        self.open_file_btn = QPushButton("Browse")
        self.open_file_btn.clicked.connect(self.filedialogopen)
        bottom_actions.addWidget(self.open_file_btn)

        #self.save_file_btn = QPushButton("Save file")
        #self.save_file_btn.clicked.connect(self.filedialogsave)
        #bottom_actions.addWidget(self.save_file_btn)

        # ALGORITHM DROPDOWN MENU 
        algo_trans = self.translations["buttons"]["algorithm"]
        self.algo_button = QPushButton(algo_trans)
        self.algo_dropdown = QMenu()
        for algo in ENC_ALGORITHMS:
            self.algo_dropdown.addAction(algo)
            self.algo_dropdown.addSeparator()
        self.algo_button.setMenu(self.algo_dropdown)
        bottom_actions.addWidget(self.algo_button)

        # ENCRYPTION KEY INPUT AND CONFIRM 
        self.text_box_enc_text = PasswordEdit(self)
        self.text_box_enc_text_confirm = PasswordEdit(self)
        bottom_actions.addWidget(self.text_box_enc_text)
        bottom_actions.addWidget(self.text_box_enc_text_confirm)

        # SALT INPUT
        self.salt_insert_box = PasswordEdit(self)
        bottom_actions.addWidget(self.salt_insert_box)

        # ENCRYPT BUTTON
        enc_trans = self.translations["buttons"]["final_encrypt"]
        self.encrypt_button = QPushButton(enc_trans)
        bottom_actions.addWidget(self.encrypt_button)

        main = QWidget()
        main.setLayout(bottom_actions)
        return main
