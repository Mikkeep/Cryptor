import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from qtwidgets import PasswordEdit

from crypto import decrypt
from .file_dialog import FileDialog
from constants import ENC_ALGORITHMS, ENC_ALGORITHMS_FILES, inprogresslist


class Decrypt_page:
    def __init__(self, translations, mainwindow):
        self.translations = translations
        self.enc_key = ""
        self.salt = ""
        self.filepath = ""
        self.chosen_algo = ""
        self.parent_win = mainwindow

    def button_dec_t(self):
        self.bottom_widget_dec.setCurrentIndex(0)

    def button_dec_f(self):
        self.bottom_widget_dec.setCurrentIndex(1)

    def decryption(self):
        """
        This method handles the frame for the entire decrypt tab
        """
        final_layout = QVBoxLayout()

        # DEFINE TOP WIDGET (TABS AND SWITCHING BETWEEN THEM)
        dec_button_text = self.translations["buttons"]["decrypt_text"]
        dec_button_files = self.translations["buttons"]["decrypt_files"]

        self.btn_dec_t = QPushButton(f"{dec_button_text}")
        self.btn_dec_t.setObjectName("btn_dec_t")
        self.btn_dec_t.clicked.connect(self.button_dec_t)
        self.btn_dec_f = QPushButton(f"{dec_button_files}")
        self.btn_dec_f.setObjectName("btn_dec_f")
        self.btn_dec_f.clicked.connect(self.button_dec_f)

        top_actions = QHBoxLayout()
        top_actions.setSpacing(0)
        top_actions.setContentsMargins(0, 16, 0, 0)
        top_actions.addWidget(self.btn_dec_t)
        top_actions.addWidget(self.btn_dec_f)
        self.top_widget_dec = QWidget()
        self.top_widget_dec.setLayout(top_actions)

        # DEFINE BOTTOM WIDGET (TAB CONTENTS)
        self.tab_dec_t = self.tab_dec_text()
        self.tab_dec_f = self.tab_dec_files()
        self.bottom_widget_dec = QTabWidget()
        self.bottom_widget_dec.tabBar().setObjectName("DecryptionTab")

        self.bottom_widget_dec.addTab(self.tab_dec_t, "")
        self.bottom_widget_dec.addTab(self.tab_dec_f, "")

        self.bottom_widget_dec.setCurrentIndex(0)  # default to text decryption tab

        # add top and bottom widgets to layout
        final_layout.addWidget(self.top_widget_dec)
        final_layout.addWidget(self.bottom_widget_dec)

        # Finish layout
        main = QWidget()
        main.setLayout(final_layout)

        return main

    def tab_dec_text(self):
        """
        This method handles the text decryption tab
        """
        # init layout and set suitable column widths
        layout = QGridLayout()

        # INSERT TEXT LABEL
        text_ins_label = QLabel(self.translations["labels"]["insert_text_dec"])
        text_ins_label.setObjectName(
            "large_label"
        )  # set object name for qss tag effects
        text_ins_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(text_ins_label, 0, 0, 1, 3)
        # INSERT TEXT BOX
        text_insert = QLineEdit()
        layout.addWidget(text_insert, 0, 3, 1, 7)

        # ALGORITHM LABEL
        algo_label = QLabel(self.translations["labels"]["set_dec_algorithm"])
        layout.addWidget(algo_label, 1, 1, 1, 3)
        # ALGORITHM DROPDOWN MENU
        self.algo_button_ttab = QPushButton(self.translations["buttons"]["algorithm"])
        self.algo_dropdown = QMenu()
        for algo in ENC_ALGORITHMS:
            self.algo_dropdown.addAction(algo)
            self.algo_dropdown.addSeparator()
        self.algo_button_ttab.setMenu(self.algo_dropdown)
        self.algo_dropdown.triggered.connect(self.algorithms_text_tab)
        layout.addWidget(self.algo_button_ttab, 1, 4, 1, 3)

        # ENCRYPTION SALT LABEL
        self.enc_salt_label = QLabel(self.translations["labels"]["salt_label"])
        layout.addWidget(self.enc_salt_label, 2, 1, 1, 1)
        # ENCRYPTION SALT INPUT
        self.text_box_salt_text = PasswordEdit()
        layout.addWidget(self.text_box_salt_text, 2, 3, 1, 6)

        # DECRYPT BUTTON
        decrypt_button = QPushButton(self.translations["buttons"]["final_decrypt"])
        layout.addWidget(decrypt_button, 3, 2, 1, 6)

        main = QWidget()
        main.setLayout(layout)
        return main

    def filedialogopen(self):
        self._files = FileDialog().fileOpen()
        self.filepath = self._files

    def filedialogsave(self):
        self._save = FileDialog().fileSave()

    # Decrypt parameters set and function call
    def decrypt_file(self):
        self.enc_key = self.text_box_dec_text.text()
        self.salt = self.text_box_salt_text.text()
        salt = self.salt
        print("salt:", salt)
        filepath = self.filepath
        fileout = os.path.basename(self.filepath)
        enc_key = self.enc_key
        print(enc_key)
        # File out gets the name of the file for saving the file
        if self.chosen_algo == "AES":
            decryptor = decrypt.Decryption(password=enc_key, salt=salt)
            result = decryptor.decrypt_with_aes(filepath, fileout)
            if result == -1:
                print("failed decrypting")
                failed_decrypt = self.translations["prompts"]["failed_decrypt"]
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(failed_decrypt)
                msg.exec_()
                return
            inprogresslist.append(f"Decrypted: {fileout}")
            progress = self.translations["prompts"]["ready"]
            self.parent_win.right_layout.clear()
            self.parent_win.right_layout.addItems(
                [f"{progress} ({len(inprogresslist)})"]
            )
            self.parent_win.right_layout.addItems(inprogresslist)
            self.parent_win.right_layout.setHidden(False)
            return
        if self.chosen_algo == "RSA":
            decryptor = decrypt.Decryption(password=enc_key, salt=salt)
            result = decryptor.decrypt_with_rsa(
                filename=filepath, priv_key="private.pem", fileout=fileout
            )
            if result == -2:
                no_RSA_keys = self.translations["prompts"]["no_rsa_keys"]
                print("Cant open key file")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(no_RSA_keys)
                msg.exec_()
                return
            if result == -1:
                print("failed decrypting")
                failed_decrypt = self.translations["prompts"]["failed_decrypt"]
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(failed_decrypt)
                msg.exec_()
                return
            inprogresslist.append(f"Decrypted: {fileout}")
            progress = self.translations["prompts"]["ready"]
            self.parent_win.right_layout.clear()
            self.parent_win.right_layout.addItems(
                [f"{progress} ({len(inprogresslist)})"]
            )
            self.parent_win.right_layout.addItems(inprogresslist)
            self.parent_win.right_layout.setHidden(False)
            return
        if self.chosen_algo == "Chacha":
            decryptor = decrypt.Decryption(password=enc_key, salt=salt)
            result = decryptor.decrypt_with_chacha(filepath, fileout)
            if result == -1:
                print("failed decrypting")
                failed_decrypt = self.translations["prompts"]["failed_decrypt"]
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(failed_decrypt)
                msg.exec_()
                return
            inprogresslist.append(f"Decrypted: {fileout}")
            progress = self.translations["prompts"]["ready"]
            self.parent_win.right_layout.clear()
            self.parent_win.right_layout.addItems(
                [f"{progress} ({len(inprogresslist)})"]
            )
            self.parent_win.right_layout.addItems(inprogresslist)
            self.parent_win.right_layout.setHidden(False)
            return
        # Filepath is the path for the file
        # Fileout is the name of the file, comes out with added
        # .dec prefix after decryption
        return

    def algorithms(self, algorithm):
        """
        Change the encryption button text to chosen algorithm
        """
        disabled_password = self.translations["prompts"]["encryption_disabled"]
        disabled_salt = self.translations["prompts"]["salt_disabled"]
        self.chosen_algo = algorithm.text()
        self.algo_button.setText(self.chosen_algo)
        if self.chosen_algo == "RSA":
            self.text_box_dec_text.setDisabled(True)
            self.text_box_dec_text.setToolTip(disabled_password)
            self.text_box_salt_text.setDisabled(True)
            self.text_box_salt_text.setToolTip(disabled_salt)
        else:
            self.text_box_dec_text.setDisabled(False)
            self.text_box_dec_text.setToolTip("")
            self.text_box_dec_text.setToolTip("")
            self.text_box_salt_text.setDisabled(False)
            self.text_box_salt_text.setToolTip("")
        self.layout.update()
        return algorithm

    def algorithms_text_tab(self, algorithm):
        """
        Change the encryption button text to chosen algorithm
        """
        self.chosen_algo = algorithm.text()
        self.algo_button_ttab.setText(self.chosen_algo)
        self.layout.update()
        return algorithm

    def tab_dec_files(self):
        """
        This method handles the file decryption tab
        """
        # init layout
        self.layout = QGridLayout()
        pad = QLabel(" ")
        self.layout.addWidget(pad, 0, 0, 1, 1)
        self.layout.addWidget(pad, 0, 9, 1, 1)

        # FILE BROWSE LABEL
        open_file_label = QLabel(self.translations["labels"]["insert_file_dec"])
        open_file_label.setObjectName("large_label")
        open_file_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(open_file_label, 0, 2, 1, 3)
        # FILE BROWSE
        open_file_btn = QPushButton(self.translations["buttons"]["browse_files"])
        open_file_btn.clicked.connect(self.filedialogopen)
        self.layout.addWidget(open_file_btn, 0, 5, 1, 3)

        # ALGORITHM LABEL
        algo_label = QLabel(self.translations["labels"]["set_dec_algorithm"])
        self.layout.addWidget(algo_label, 1, 2, 1, 3)
        # ALGORITHM DROPDOWN MENU
        self.algo_button = QPushButton(self.translations["buttons"]["algorithm"])
        self.algo_dropdown = QMenu()
        self.algo_dropdown.setObjectName("algo_menu_dec")
        for algo in ENC_ALGORITHMS_FILES:
            self.algo_dropdown.addAction(algo)
            self.algo_dropdown.addSeparator()
        self.algo_button.setMenu(self.algo_dropdown)
        self.algo_dropdown.triggered.connect(self.algorithms)
        self.layout.addWidget(self.algo_button, 1, 5, 1, 3)

        # ENCRYPTION KEY LABEL
        self.enc_key_label = QLabel(self.translations["labels"]["encryption_key_label"])
        self.layout.addWidget(self.enc_key_label, 2, 1, 1, 2)
        # ENCRYPTION KEY INPUT
        self.text_box_dec_text = PasswordEdit()
        self.layout.addWidget(self.text_box_dec_text, 2, 3, 1, 6)

        # ENCRYPTION SALT LABEL
        self.enc_salt_label = QLabel(self.translations["labels"]["salt_label"])
        self.layout.addWidget(self.enc_salt_label, 3, 1, 1, 2)
        # ENCRYPTION SALT INPUT
        self.text_box_salt_text = PasswordEdit()
        self.layout.addWidget(self.text_box_salt_text, 3, 3, 1, 6)

        # DECRYPT BUTTON
        decrypt_button = QPushButton(self.translations["buttons"]["final_decrypt"])
        decrypt_button.clicked.connect(self.decrypt_file)
        self.layout.addWidget(decrypt_button, 4, 2, 1, 6)

        # finish layout
        main = QWidget()
        main.setLayout(self.layout)
        return main
