from PyQt5.QtWidgets import *
from .file_dialog import FileDialog
from constants import ENC_ALGORITHMS
from qtwidgets import PasswordEdit



class Decrypt_page:
    def __init__(self, translations):
        self.translations = translations

    def button_dec_t(self):
        self.bottom_widget_dec.setCurrentIndex(0)

    def button_dec_f(self):
        self.bottom_widget_dec.setCurrentIndex(1)

    def decryption(self):
        final_layout = QVBoxLayout()

        dec_button_text = self.translations["buttons"]["decrypt_text"]
        dec_button_files = self.translations["buttons"]["decrypt_files"]

        self.btn_dec_t = QPushButton(f"{dec_button_text}")
        self.btn_dec_t.clicked.connect(self.button_dec_t)
        self.btn_dec_f = QPushButton(f"{dec_button_files}")
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

    def tab_dec_text(self):
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
        self.text_box_dec_text = PasswordEdit(self)
        #self.text_box_dec_text_confirm = PasswordEdit(self)
        bottom_layout.addWidget(self.text_box_dec_text)
        #bottom_layout.addWidget(self.text_box_dec_text_confirm)

        # DECRYPT BUTTON
        dec_trans = self.translations["buttons"]["final_decrypt"]
        self.decrypt_button = QPushButton(dec_trans)
        bottom_layout.addWidget(self.decrypt_button)
        
        main = QWidget()
        main.setLayout(bottom_layout)
        return main

    def filedialogopen(self):
        self._files = FileDialog().fileOpen()

    def filedialogsave(self):
        self._save = FileDialog().fileSave()

    def tab_dec_files(self):
        bottom_layout = QVBoxLayout()

		# FILE BROWSE
        self.open_file_btn = QPushButton("Browse")
        self.open_file_btn.clicked.connect(self.filedialogopen)
        bottom_layout.addWidget(self.open_file_btn)
        
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
        self.text_box_dec_text = PasswordEdit(self)
        #self.text_box_dec_text_confirm = PasswordEdit(self)
        bottom_layout.addWidget(self.text_box_dec_text)
        #bottom_layout.addWidget(self.text_box_dec_text_confirm)

        # DECRYPT BUTTON
        dec_trans = self.translations["buttons"]["final_decrypt"]
        self.decrypt_button = QPushButton(dec_trans)
        bottom_layout.addWidget(self.decrypt_button)
        
        main = QWidget()
        main.setLayout(bottom_layout)
        return main
