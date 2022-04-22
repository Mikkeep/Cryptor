import os
from PyQt5.QtWidgets import *
from constants import *
from qtwidgets import PasswordEdit
from .file_dialog import FileDialog
from constants import ENC_ALGORITHMS, ENC_ALGORITHMS_FILES
from crypto import encrypt
from utils import check_encryption_defaults


class Encrypt_page:
    def __init__(self, translations, mainwindow):
        # Define used class parameters to be set in the selections
        self.translations = translations
        self.defaults = check_encryption_defaults(db_location)
        self.filepath = ""
        self.salt = ""
        self.enc_key = ""
        self.parent_win = mainwindow
        if self.defaults["default_hash"] != "":
            self.chosen_algo = self.defaults["default_hash"]
        else:
            self.chosen_algo = ""
        if self.defaults["default_algo"] != "":
            self.chosen_algorithm = self.defaults["default_algo"]
        else:
            self.chosen_algorithm = ""

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

        self.bottom_widget.setCurrentIndex(0)  # default to the text tab

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
        layout.addWidget(text_to_enc_label, 0, 0, 1, 1)
        # INSERT TEXT BOX
        self.text_insert = QLineEdit()
        layout.addWidget(self.text_insert, 0, 1, 1, 3)

        # ALGORITHM SET LABEL
        algo_text_label = QLabel(self.translations["labels"]["set_enc_algorithm"])
        layout.addWidget(algo_text_label, 1, 0, 1, 1)
        # ALGORITHM DROPDOWN MENU
        algo_trans = self.translations["buttons"]["algorithm"]
        self.algo_button_ttab = QPushButton(algo_trans)
        self.algo_dropdown = QMenu()
        for algo in ENC_ALGORITHMS:
            self.algo_dropdown.addAction(algo)
            self.algo_dropdown.addSeparator()
        self.algo_button_ttab.setMenu(self.algo_dropdown)
        self.algo_dropdown.triggered.connect(self.algorithms_text)
        if self.defaults["default_hash"] != "":
            self.algo_button_ttab.setText(self.defaults["default_hash"])
        layout.addWidget(self.algo_button_ttab, 1, 1, 1, 3)

        # ENCRYPTION KEY INPUT AND CONFIRM LABELS
        enc_text_label = QLabel(self.translations["labels"]["encryption_key_label"])
        enc_conf_label = QLabel(
            self.translations["labels"]["encryption_key_confirm_label"]
        )
        enc_text_label.setHidden(True)
        enc_conf_label.setHidden(True)
        layout.addWidget(enc_text_label, 2, 0, 1, 1)
        layout.addWidget(enc_conf_label, 2, 2)
        # ENCRYPTION KEY INPUT AND CONFIRM
        self.text_box_enc_text_ttab = PasswordEdit()
        self.text_box_enc_text_ttab.setHidden(True)
        if self.defaults["default_key"] != "":
            self.text_box_enc_text_ttab.setText(self.defaults["default_key"])
        self.text_box_enc_text_confirm_ttab = PasswordEdit()
        self.text_box_enc_text_confirm_ttab.setHidden(True)
        if self.defaults["default_key"] != "":
            self.text_box_enc_text_confirm_ttab.setText(self.defaults["default_key"])
        layout.addWidget(self.text_box_enc_text_ttab, 2, 1)
        layout.addWidget(self.text_box_enc_text_confirm_ttab, 2, 3)

        # SALT INPUT LABEL
        salt_label = QLabel(self.translations["labels"]["salt_label"])
        layout.addWidget(salt_label, 3, 0, 1, 1)
        # SALT INPUT
        self.salt_insert_box_ttab = PasswordEdit()
        if self.defaults["default_salt"] != "":
            self.salt_insert_box_ttab.setText(self.defaults["default_salt"])
        layout.addWidget(self.salt_insert_box_ttab, 3, 1, 1, 3)

        # ENCRYPT BUTTON
        enc_trans = self.translations["buttons"]["final_encrypt"]
        encrypt_button = QPushButton(enc_trans)
        encrypt_button.clicked.connect(self.encrypt_text)
        self.encrypt_result = QLineEdit()
        self.encrypt_result.setHidden(True)
        layout.addWidget(encrypt_button, 4, 0, 1, 4)
        layout.addWidget(self.encrypt_result, 5, 0, 1, 4)

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
        fileout = os.path.basename(self.filepath)
        inprogresslist.append(fileout)
        progress = self.translations["prompts"]["in_progress"]
        self.parent_win.right_layout.clear()
        self.parent_win.right_layout.addItems([f"{progress} ({len(inprogresslist)})"])
        self.parent_win.right_layout.addItem(fileout)

    def filedialogsave(self):
        """
        File save method
        """
        self._save = FileDialog().fileSave()

    # Encrypt parameters set and function call
    def encrypt_file(self):
        self.enc_key = self.text_box_enc_text.text()
        self.enc_key_confirm = self.text_box_enc_text_confirm.text()
        self.salt = self.salt_insert_box.text()
        filepath = self.filepath
        fileout = os.path.basename(self.filepath)
        salt = self.salt
        enc_key = self.enc_key
        print(self.chosen_algorithm)
        if str(self.enc_key) != str(self.enc_key_confirm):
            pwd_mismatch = self.translations["prompts"]["password_mismatch"]
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(pwd_mismatch)
            display = msg.exec_()
            return
        # File out gets the name of the file for saving the file
        if self.chosen_algorithm == "AES":
            encryptor = encrypt.Encryption(password=enc_key, salt=salt)
            encryptor.encrypt_with_aes(filepath, fileout)
        if self.chosen_algorithm == "RSA":
            encryptor = encrypt.Encryption(password=enc_key, salt=salt)
            encryptor.encrypt_with_rsa(filepath, fileout)
        if self.chosen_algorithm == "ChaCha20":
            encryptor = encrypt.Encryption(password=enc_key, salt=salt)
            encryptor.encrypt_with_chacha(filepath, fileout)
        # Filepath is the path for the file
        # Fileout is the name of the file, comes out with added
        # _encryted prefix after ecnryption
        inprogresslist.clear()
        progress = "ready: "
        self.parent_win.right_layout.insertItem(7, f"{progress} ({len(inprogresslist)})")
        self.parent_win.right_layout.addItem("Olen valmis")
        return

    def encrypt_text(self):
        result = ""
        self.encrypt_result.setHidden(False)
        text_hasher = encrypt.Encryption(salt=self.salt_insert_box_ttab.text())
        if self.chosen_algo == "MD5":
            result = text_hasher.hash_with_md5(self.text_insert.text())
        if self.chosen_algo == "SHA-256":
            result = text_hasher.hash_with_sha256(self.text_insert.text())
        if self.chosen_algo == "SHA-512":
            result = text_hasher.hash_with_sha512(self.text_insert.text())
        if self.chosen_algo == "SHA3-512":
            result = text_hasher.hash_with_sha3_512(self.text_insert.text())
        self.encrypt_result.setText(result)

    def algorithms(self, algorithm):
        disabled_password = self.translations["prompts"]["encryption_disabled"]
        disabled_salt = self.translations["prompts"]["salt_disabled"]
        self.chosen_algorithm = algorithm.text()
        self.algo_button.setText(self.chosen_algorithm)
        if self.chosen_algorithm == "RSA":
            self.text_box_enc_text.setDisabled(True)
            self.text_box_enc_text.setToolTip(disabled_password)
            self.text_box_enc_text_confirm.setDisabled(True)
            self.text_box_enc_text_confirm.setToolTip(disabled_password)
            self.salt_insert_box.setDisabled(True)
            self.salt_insert_box.setToolTip(disabled_salt)
        else:
            self.text_box_enc_text.setDisabled(False)
            self.text_box_enc_text.setToolTip("")
            self.text_box_enc_text_confirm.setDisabled(False)
            self.text_box_enc_text.setToolTip("")
            self.salt_insert_box.setDisabled(False)
            self.text_box_enc_text.setToolTip("")
        self.layout.update()
        return algorithm

    def algorithms_text(self, algorithm):
        """
        Change the encryption button text to chosen algorithm
        """
        self.chosen_algo = algorithm.text()
        self.algo_button_ttab.setText(self.chosen_algo)
        self.layout.update()
        return algorithm

    def tab_enc_files(self):
        """
        This method handles the file encryption tab
        """
        # init layout and set all column widths to suit the layout
        self.layout = QGridLayout()
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 2)
        self.layout.setColumnStretch(2, 1)
        self.layout.setColumnStretch(3, 2)

        # FILE BROWSER LABEL
        file_browse_label = QLabel(self.translations["labels"]["browse_file_enc"])
        self.layout.addWidget(file_browse_label, 0, 0, 1, 1)

        # INSERT FILE BROWSER
        file_browse_btn = QPushButton(self.translations["buttons"]["browse_files"])
        file_browse_btn.clicked.connect(self.filedialogopen)
        self.layout.addWidget(file_browse_btn, 0, 1, 1, 3)

        # ALGORITHM SET LABEL
        self.algo_text_label = QLabel(self.translations["labels"]["set_enc_algorithm"])
        self.layout.addWidget(self.algo_text_label, 1, 0, 1, 1)
        # ALGORITHM DROPDOWN MENU
        self.algo_button = QPushButton(self.translations["buttons"]["algorithm"])
        self.algo_dropdown = QMenu()
        for algo in ENC_ALGORITHMS_FILES:
            self.algo_dropdown.addAction(algo)
            self.algo_dropdown.addSeparator()
        self.algo_button.setMenu(self.algo_dropdown)
        self.algo_dropdown.triggered.connect(self.algorithms)
        if self.defaults["default_algo"] != "":
            self.algo_button.setText(self.defaults["default_algo"])
        #        if self.algo_dropdown.triggered:
        #            self.algo_button.setText(self.chosen_algo)
        #            self.layout.update()
        self.layout.addWidget(self.algo_button, 1, 1, 1, 3)

        # ENCRYPTION KEY INPUT AND CONFIRM LABELS
        enc_text_label = QLabel(self.translations["labels"]["encryption_key_label"])
        enc_conf_label = QLabel(
            self.translations["labels"]["encryption_key_confirm_label"]
        )

        self.layout.addWidget(enc_text_label, 2, 0, 1, 1)
        self.layout.addWidget(enc_conf_label, 2, 2, 1, 1)
        # ENCRYPTION KEY INPUT AND CONFIRM
        self.text_box_enc_text = PasswordEdit()
        if self.defaults["default_key"] != "":
            self.text_box_enc_text.setText(self.defaults["default_key"])
        self.text_box_enc_text_confirm = PasswordEdit()
        if self.defaults["default_key"] != "":
            self.text_box_enc_text_confirm.setText(self.defaults["default_key"])
        self.layout.addWidget(self.text_box_enc_text, 2, 1, 1, 1)
        self.layout.addWidget(self.text_box_enc_text_confirm, 2, 3, 1, 1)

        # SALT INPUT LABEL
        salt_label = QLabel(self.translations["labels"]["salt_label"])
        self.layout.addWidget(salt_label, 3, 0, 1, 1)
        # SALT INPUT
        self.salt_insert_box = PasswordEdit()
        if self.defaults["default_salt"] != "":
            self.salt_insert_box.setText(self.defaults["default_salt"])
        self.layout.addWidget(self.salt_insert_box, 3, 1, 1, 3)

        # ENCRYPT BUTTON
        self.encrypt_button = QPushButton(self.translations["buttons"]["final_encrypt"])
        self.layout.addWidget(self.encrypt_button, 4, 0, 1, 4)
        self.encrypt_button.clicked.connect(self.encrypt_file)

        # finish and set layout
        self.main = QWidget()
        self.main.setLayout(self.layout)
        return self.main
