from PyQt5.QtWidgets import QFileDialog, QWidget
import sys


class FileDialog(QWidget):

    def __init__(self):
        super().__init__()
    
    def fileOpen(self):
        opening_options = QFileDialog.Options()
        get_files, meta = QFileDialog.getOpenFileName(self, options=opening_options)
        if get_files:
            print(get_files)
            return get_files
    
    def fileSave(self):
        saving_options = QFileDialog.Options()
        save_file, meta = QFileDialog.getSaveFileName(self, options=saving_options)
        if save_file:
            print("saved ", save_file)
