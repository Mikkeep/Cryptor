from PyQt5.QtWidgets import *
from constants import *
from utils import *
from crypto import generate_salt


class SaltWindow(QWidget):
    def __init__(self, translation, window):
        super().__init__()
        layout = QVBoxLayout()

        self.settings_translate = translation
        self.count = 0
        self.coordinates = []
        self.final_val = ""
        self.parent_window = window
        self.setMouseTracking(True)

        self.setWindowTitle("Set salt value by clicking three times")

        self.setLayout(layout)

        self.Width = 400
        self.height = int(0.8 * self.Width)
        self.setFixedSize(self.Width, self.height)

        # center the window relative to screensize
        centering = self.frameGeometry()
        centerOfScreen = QDesktopWidget().availableGeometry().center()
        centering.moveCenter(centerOfScreen)
        self.move(centering.topLeft())

    def mousePressEvent(self, event):
        self.count += 1
        if self.count >= 3:
            save_salt = generate_salt.salt_generator().generate_salt_from_coords(
                *self.coordinates
            )
            self.final_val = str(save_salt)
            print(self.final_val)
            self.parent_window.chosen_salt = self.final_val
            self.parent_window.text_box_salt.setText(self.parent_window.chosen_salt)
            self.close()
        super().mousePressEvent(event)
        self.coordinates.append(event.x())
        self.coordinates.append(event.y())

    def get_final_val(self):
        return self.final_val
