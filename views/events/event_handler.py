import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFileDialog


class EventHandler:
    
    def open_directory(self):
        directory_name = QFileDialog.getExistingDirectory(self, "Select Directory", "", QFileDialog.ShowDirsOnly)
        if directory_name:
            print(directory_name)


    def open_files(self):
        pass

    
    





