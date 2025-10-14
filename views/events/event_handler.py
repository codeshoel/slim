import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFileDialog


class EventHandler():
    
    def open_directory(self):
        options = QFileDialog.ShowDirsOnly
        file_name = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', options)
        if file_name:
            print(file_name)

    # def set_input_text(self, text_input=None):
    #     return text_input

    def open_files(self):
        pass

    
    





