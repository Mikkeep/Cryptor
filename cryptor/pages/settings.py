from PyQt5.QtWidgets import *
from qtwidgets import PasswordEdit
from constants import *
from utils import *
from PyQt5.QtGui import QIcon


class SettingsWindow(QWidget):
    def __init__(self, translation):
        super().__init__()
        layout = QVBoxLayout()
        self.chosen_algo = ""
        self.chosen_hash = ""
        self.chosen_salt = ""
        self.chosen_key = ""
        self.settings_translate = translation
        enc_key = self.settings_translate["buttons"]["encryption_key_prompt"]
        enc_key_confirm = self.settings_translate["buttons"]["encryption_key_confirm"]
        algorithm = self.settings_translate["buttons"]["algorithm"]
        hash = self.settings_translate["buttons"]["hash"]
        salt = self.settings_translate["buttons"]["salt"]
        close_btn = self.settings_translate["prompts"]["close_button"]

        self.setWindowIcon(QIcon(IMG_LOCATION + "win_icon.png"))
        self.setWindowTitle("Set default encryption settings")

        self.hash = QPushButton(hash)
        self.algorithm = QPushButton(algorithm)
        self.text_box_salt = PasswordEdit(self)
        self.text_box_salt.setPlaceholderText(salt)
        self.text_box_enc_text = PasswordEdit(self)
        self.text_box_enc_text.setPlaceholderText(enc_key)
        self.text_box_enc_text_confirm = PasswordEdit(self)
        self.text_box_enc_text_confirm.setPlaceholderText(enc_key_confirm)
        self.close_button = QPushButton(close_btn)
        self.close_button.clicked.connect(self.close_settings)
        # Define Hash functions menu
        self.menu = QMenu(self)
        self.menu.addAction("MD5")
        self.menu.addSeparator()
        self.menu.addAction("SHA-256")
        self.menu.addSeparator()
        self.menu.addAction("SHA-512")
        self.menu.addSeparator()
        self.menu.addAction("SHA3-512")
        self.hash.setMenu(self.menu)
        self.menu.triggered.connect(self.hashes)
        # Define Algorithms functions menu
        self.menu_algo = QMenu(self)
        self.menu_algo.addAction("ChaCha20")
        self.menu_algo.addSeparator()
        self.menu_algo.addAction("RSA")
        self.menu_algo.addSeparator()
        self.menu_algo.addAction("AES")
        self.algorithm.setMenu(self.menu_algo)
        self.menu_algo.triggered.connect(self.algorithms)
        layout.addWidget(self.hash)
        layout.addWidget(self.algorithm)
        #        layout.addWidget(self.salt)
        layout.addWidget(self.text_box_salt)
        layout.addWidget(self.text_box_enc_text)
        layout.addWidget(self.text_box_enc_text_confirm)
        layout.addSpacing(50)
        layout.addWidget(self.close_button)
        self.setLayout(layout)

        self.Width = 700
        self.height = int(0.8 * self.Width)
        self.setFixedSize(self.Width, self.height)
        # center the window relative to screensize
        centering = self.frameGeometry()
        centerOfScreen = QDesktopWidget().availableGeometry().center()
        centering.moveCenter(centerOfScreen)
        self.move(centering.topLeft())

    def hashes(self, language):
        self.chosen_hash = language.text()
        print(language.text())
        return language

    def algorithms(self, language):
        self.chosen_algo = language.text()
        print(language.text())
        return language

    def close_settings(self, event):
        pwd_mismatch = self.settings_translate["prompts"]["password_mismatch"]
        confirm_no_enc_key_set = self.settings_translate["prompts"][
            "confirm_no_password"
        ]
        no_enc_key_prompt = self.settings_translate["prompts"]["no_enc_key"]
        print("Chosen algorithm: ", self.chosen_algo)
        print("Chosen salt: ", self.text_box_salt.text())
        print("Chosen enc key: ", self.text_box_enc_text.text())
        print("Chosen enc key: ", self.text_box_enc_text_confirm.text())
        if str(self.text_box_enc_text.text()) == str(
            self.text_box_enc_text_confirm.text()
        ):
            if (
                str(self.text_box_enc_text.text()) == ""
                and str(self.text_box_enc_text_confirm.text()) == ""
            ):
                confirm_no_pwd = QMessageBox.question(
                    self,
                    no_enc_key_prompt,
                    confirm_no_enc_key_set,
                    QMessageBox.Yes | QMessageBox.No,
                )
                if confirm_no_pwd == QMessageBox.Yes:
                    defaults = {"hash": "", "algorithm": "", "salt": "", "key": ""}
                    if self.chosen_hash != "":
                        defaults["hash"] = self.chosen_hash
                    if self.chosen_algo != "":
                        defaults["algorithm"] = self.chosen_algo
                    if self.text_box_salt.text() != "":
                        defaults["salt"] = self.text_box_salt.text()
                    if self.text_box_enc_text.text() != "":
                        defaults["key"] = self.text_box_enc_text.text()
                    write_encryption_defaults(
                        db_location,
                        (
                            defaults["hash"],
                            defaults["algorithm"],
                            defaults["salt"],
                            defaults["key"],
                        ),
                    )
                    self.close()
                    return
                return
        if (
            str(self.text_box_enc_text.text()) == ""
            and str(self.text_box_enc_text_confirm.text()) == ""
        ):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(pwd_mismatch)
            display = msg.exec_()
            return

        defaults = {"hash": "", "algorithm": "", "salt": "", "key": ""}
        if self.chosen_hash != "":
            defaults["hash"] = self.chosen_hash
        if self.chosen_algo != "":
            defaults["algorithm"] = self.chosen_algo
        if self.text_box_salt.text() != "":
            defaults["salt"] = self.text_box_salt.text()
        if self.text_box_enc_text.text() != "":
            defaults["key"] = self.text_box_enc_text.text()
        write_encryption_defaults(
            db_location,
            (
                defaults["hash"],
                defaults["algorithm"],
                defaults["salt"],
                defaults["key"],
            ),
        )
        self.close()
