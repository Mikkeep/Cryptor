from PyQt5.QtWidgets import *

class Decrypt_page():
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
		bottom_layout.addWidget(QLabel(":)"))
		#        bottom_layout.addStretch(5)
		main = QWidget()
		main.setLayout(bottom_layout)
		return main

	def tab_dec_files(self):
		bottom_actions = QVBoxLayout()
		bottom_actions.addWidget(QLabel("(:"))
		bottom_actions.addStretch(5)
		main = QWidget()
		main.setLayout(bottom_actions)
		return main