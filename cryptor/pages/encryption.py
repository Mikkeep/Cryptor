import os
from PyQt5.QtWidgets import *
from qtwidgets import PasswordEdit
from .file_dialog import FileDialog
from constants import ENC_ALGORITHMS
from crypto import encrypt


class Encrypt_page:
    def __init__(self, translations):
        # Define used class parameters to be set in the selections
        self.translations = translations
        self.filepath = ""
        self.salt = ""
        self.enc_key = ""

    def button_enc_t(self):
        self.bottom_widget.setCurrentIndex(0)

    def button_enc_f(self):
        self.bottom_widget.setCurrentIndex(1)

    def encryption(self):
        """
        This method handles frame for the entire encrypt tab
        """
        final_layout = QVBoxLayout()

        # DEFINE TOP WIDGET (TABS AND SWITCHING BETWEEN THEM)
        enc_button_text = self.translations["buttons"]["encrypt_text"]
        enc_button_files = self.translations["buttons"]["encrypt_files"]
        
        btn_enc_t = QPushButton(f"{enc_button_text}")
        btn_enc_t.clicked.connect(self.button_enc_t)

        btn_enc_f = QPushButton(f"{enc_button_files}")
        btn_enc_f.clicked.connect(self.button_enc_f)
        top_actions = QHBoxLayout()
        top_actions.addWidget(btn_enc_t)
        top_actions.addWidget(btn_enc_f)

        self.top_widget = QWidget()
        self.top_widget.setLayout(top_actions)

        # DEFINE BOTTOM WIDGET (TAB CONTENTS)
        self.tab_enc_t = self.tab_enc_text()
        self.tab_enc_f = self.tab_enc_files()

        self.bottom_widget = QTabWidget()
        self.bottom_widget.tabBar().setObjectName("EncryptionTab")

        self.bottom_widget.addTab(self.tab_enc_t, "")
        self.bottom_widget.addTab(self.tab_enc_f, "")

        self.bottom_widget.setCurrentIndex(0) # default to the text tab

        # Add top and bottom parts to the layout
        final_layout.addWidget(self.top_widget)
        final_layout.addWidget(self.bottom_widget)

        # Finish layout
        main = QWidget()
        main.setLayout(final_layout)

        return main

    def tab_enc_text(self):
        """
        This method handles the text encryption tab
        """
        # init layout and set all column widths to suit the layout
        layout = QGridLayout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 2)

        # INSERT TEXT LABEL
        text_to_enc_label = QLabel(self.translations["labels"]["insert_text_enc"])
        layout.addWidget(text_to_enc_label, 0, 0)
        # INSERT TEXT BOX
        text_insert = QLineEdit()
        layout.addWidget(text_insert, 0, 1, 1, 3)
        
        # ALGORITHM SET LABEL
        algo_text_label = QLabel(self.translations["labels"]["set_enc_algorithm"])
        layout.addWidget(algo_text_label, 1, 0, 1, 1)
        # ALGORITHM DROPDOWN MENU 
        algo_trans = self.translations["buttons"]["algorithm"]
        algo_button = QPushButton(algo_trans)
        algo_dropdown = QMenu()
        for algo in ENC_ALGORITHMS:
            algo_dropdown.addAction(algo)
            algo_dropdown.addSeparator()
        algo_button.setMenu(algo_dropdown)
        layout.addWidget(algo_button, 1, 1, 1, 3)

        # ENCRYPTION KEY INPUT AND CONFIRM LABELS
        enc_text_label = QLabel(self.translations["labels"]["encryption_key_label"])
        enc_conf_label = QLabel(self.translations["labels"]["encryption_key_confirm_label"])
        layout.addWidget(enc_text_label, 2, 0, 1, 1)
        layout.addWidget(enc_conf_label, 2, 2)
        # ENCRYPTION KEY INPUT AND CONFIRM 
        text_box_enc_text = PasswordEdit()
        text_box_enc_text_confirm = PasswordEdit()
        layout.addWidget(text_box_enc_text, 2, 1)
        layout.addWidget(text_box_enc_text_confirm, 2, 3)

        # SALT INPUT LABEL
        salt_label = QLabel(self.translations["labels"]["salt_label"])
        layout.addWidget(salt_label, 3, 0, 1, 1)
        # SALT INPUT
        salt_insert_box = PasswordEdit()
        layout.addWidget(salt_insert_box, 3, 1, 1, 3)

        # ENCRYPT BUTTON
        enc_trans = self.translations["buttons"]["final_encrypt"]
        encrypt_button = QPushButton(enc_trans)
        layout.addWidget(encrypt_button, 4, 0, 1, 4)
        
        # finish and set layout
        main = QWidget()
        main.setLayout(layout)
        return main

    def filedialogopen(self):
        """
        File dialog opening method
        """
        self._files = FileDialog().fileOpen()
        self.filepath = self._files

    def filedialogsave(self):
        """
        File save method
        """
        self._save = FileDialog().fileSave()

    #Encrypt parameters set and function call
    def encrypt_file(self, filepath="", salt="", enc_key=""):
        self.enc_key = self.text_box_enc_text_confirm.text()
        self.salt = self.salt_insert_box.text()
        filepath = self.filepath
        # File out gets the name of the file for saving the file
        fileout = os.path.basename(self.filepath)
        print(fileout)
        salt = self.salt
        enc_key = self.enc_key
        print("clicked encrypt")
        print("Filepath: ", self.filepath)
        print("used password: ", self.enc_key)
        print("used salt: ", self.salt)
        encryptor = encrypt.Encryption(password=enc_key, salt=salt)
        # Filepath is the path for the file
        # Fileout is the name of the file, comes out with added
        # _encryted prefix after ecnryption
        encryptor.encrypt_with_aes(filepath, fileout)
        print("Done encrypting")

    def tab_enc_files(self):
        """
        This method handles the file encryption tab
        """
        # init layout and set all column widths to suit the layout
        layout = QGridLayout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 2)

        # FILE BROWSER LABEL
        file_browse_label = QLabel(self.translations["labels"]["browse_file_enc"])
        layout.addWidget(file_browse_label, 0, 0, 1, 1)

        # INSERT FILE BROWSER
        file_browse_btn = QPushButton(self.translations["buttons"]["browse_files"])
        file_browse_btn.clicked.connect(self.filedialogopen)
        layout.addWidget(file_browse_btn, 0, 1, 1, 3)
        
        # ALGORITHM SET LABEL
        algo_text_label = QLabel(self.translations["labels"]["set_enc_algorithm"])
        layout.addWidget(algo_text_label, 1, 0, 1, 1)
        # ALGORITHM DROPDOWN MENU 
        algo_button = QPushButton(self.translations["buttons"]["algorithm"])
        algo_dropdown = QMenu()
        for algo in ENC_ALGORITHMS:
            algo_dropdown.addAction(algo)
            algo_dropdown.addSeparator()
        algo_button.setMenu(algo_dropdown)
        layout.addWidget(algo_button, 1, 1, 1, 3)

        # ENCRYPTION KEY INPUT AND CONFIRM LABELS
        enc_text_label = QLabel(self.translations["labels"]["encryption_key_label"])
        enc_conf_label = QLabel(self.translations["labels"]["encryption_key_confirm_label"])
        layout.addWidget(enc_text_label, 2, 0, 1, 1)
        layout.addWidget(enc_conf_label, 2, 2)
        # ENCRYPTION KEY INPUT AND CONFIRM 
        self.text_box_enc_text = PasswordEdit()
        self.text_box_enc_text_confirm = PasswordEdit()
        layout.addWidget(self.text_box_enc_text, 2, 1)
        layout.addWidget(self.text_box_enc_text_confirm, 2, 3)

        # SALT INPUT LABEL
        salt_label = QLabel(self.translations["labels"]["salt_label"])
        layout.addWidget(salt_label, 3, 0, 1, 1)
        # SALT INPUT
        self.salt_insert_box = PasswordEdit()
        layout.addWidget(self.salt_insert_box, 3, 1, 1, 3)

        # ENCRYPT BUTTON
        self.encrypt_button = QPushButton(self.translations["buttons"]["final_encrypt"])
        layout.addWidget(self.encrypt_button, 4, 0, 1, 4)
        self.encrypt_button.clicked.connect(self.encrypt_file)
        
        # finish and set layout
        main = QWidget()
        main.setLayout(layout)
        return main