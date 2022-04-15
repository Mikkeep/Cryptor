from PyQt5.QtWidgets import *
from qtwidgets import PasswordEdit
from .file_dialog import FileDialog
from constants import ENC_ALGORITHMS


class Decrypt_page:
    def __init__(self, translations):
        self.translations = translations

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
        self.btn_dec_t.clicked.connect(self.button_dec_t)
        self.btn_dec_f = QPushButton(f"{dec_button_files}")
        self.btn_dec_f.clicked.connect(self.button_dec_f)

        top_actions = QHBoxLayout()
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

        self.bottom_widget_dec.setCurrentIndex(0) # default to text decryption tab

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
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 2)

        # INSERT TEXT LABEL
        text_ins_label = QLabel(self.translations["labels"]["insert_text_dec"])
        layout.addWidget(text_ins_label, 0, 0, 1, 1)
        # INSERT TEXT BOX
        text_insert = QLineEdit()
        layout.addWidget(text_insert, 0, 1, 1, 3)

        # ALGORITHM LABEL
        algo_label = QLabel(self.translations["labels"]["set_enc_algorithm"])
        layout.addWidget(algo_label, 1, 0, 1, 1)
        # ALGORITHM DROPDOWN MENU 
        algo_button = QPushButton(self.translations["buttons"]["algorithm"])
        algo_dropdown = QMenu()
        for algo in ENC_ALGORITHMS:
            algo_dropdown.addAction(algo)
            algo_dropdown.addSeparator()
        algo_dropdown.setStyleSheet("width: 462px;")
        algo_button.setMenu(algo_dropdown)
        layout.addWidget(algo_button, 1, 1, 1, 3)

        # ENCRYPTION KEY LABEL
        enc_key_label = QLabel(self.translations["labels"]["encryption_key_label"])
        layout.addWidget(enc_key_label, 2, 0, 1, 1)
        # ENCRYPTION KEY INPUT 
        text_box_dec_text = PasswordEdit()
        layout.addWidget(text_box_dec_text, 2, 1, 1, 3)

        # DECRYPT BUTTON
        decrypt_button = QPushButton(self.translations["buttons"]["final_decrypt"])
        layout.addWidget(decrypt_button, 3, 0, 1, 4)
        
        main = QWidget()
        main.setLayout(layout)
        return main

    def filedialogopen(self):
        self._files = FileDialog().fileOpen()

    def filedialogsave(self):
        self._save = FileDialog().fileSave()

    def tab_dec_files(self):
        """
        This method handles the file decryption tab
        """
        # init layout and set suitable column widths
        layout = QGridLayout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 2)

        # FILE BROWSE LABEL
        open_file_label = QLabel(self.translations["labels"]["insert_file_dec"])
        layout.addWidget(open_file_label, 0, 0, 1, 1)
		# FILE BROWSE
        open_file_btn = QPushButton(self.translations["buttons"]["browse_files"])
        open_file_btn.clicked.connect(self.filedialogopen)
        layout.addWidget(open_file_btn, 0, 1, 1, 3)
        
        # ALGORITHM LABEL
        algo_label = QLabel(self.translations["labels"]["set_enc_algorithm"])
        layout.addWidget(algo_label, 1, 0, 1, 1)
        # ALGORITHM DROPDOWN MENU 
        algo_button = QPushButton(self.translations["buttons"]["algorithm"])
        algo_dropdown = QMenu()
        for algo in ENC_ALGORITHMS:
            algo_dropdown.addAction(algo)
            algo_dropdown.addSeparator()
        algo_dropdown.setStyleSheet("width: 462px;")
        algo_button.setMenu(algo_dropdown)
        layout.addWidget(algo_button, 1, 1, 1, 3)

        # ENCRYPTION KEY LABEL
        enc_key_label = QLabel(self.translations["labels"]["encryption_key_label"])
        layout.addWidget(enc_key_label, 2, 0, 1, 1)
        # ENCRYPTION KEY INPUT 
        text_box_dec_text = PasswordEdit()
        layout.addWidget(text_box_dec_text, 2, 1, 1, 3)

        # DECRYPT BUTTON
        decrypt_button = QPushButton(self.translations["buttons"]["final_decrypt"])
        layout.addWidget(decrypt_button, 3, 0, 1, 4)
        
        # finish layout
        main = QWidget()
        main.setLayout(layout)
        return main
