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
        bottom_layout = QVBoxLayout()

        # INSERT TEXT BOX
        self.text_insert = QLineEdit()
        bottom_layout.addWidget(self.text_insert)
        
        # ALGORITHM DROPDOWN MENU 
        algo_trans = self.translations["buttons"]["algorithm"]
        self.algo_button = QPushButton(algo_trans)
        self.algo_dropdown = QMenu()
        for algo in ENC_ALGORITHMS:
            self.algo_dropdown.addAction(algo)
            self.algo_dropdown.addSeparator()
        self.algo_button.setMenu(self.algo_dropdown)
        bottom_layout.addWidget(self.algo_button)

        # ENCRYPTION KEY INPUT AND CONFIRM 
        self.text_box_enc_text = PasswordEdit(self)
        self.text_box_enc_text_confirm = PasswordEdit(self)
        bottom_layout.addWidget(self.text_box_enc_text)
        bottom_layout.addWidget(self.text_box_enc_text_confirm)

        # SALT INPUT
        self.salt_insert_box = PasswordEdit(self)
        bottom_layout.addWidget(self.salt_insert_box)

        # ENCRYPT BUTTON
        enc_trans = self.translations["buttons"]["final_encrypt"]
        self.encrypt_button = QPushButton(enc_trans)
        bottom_layout.addWidget(self.encrypt_button)
        
        main = QWidget()
        main.setLayout(bottom_layout)
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
