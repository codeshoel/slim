import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFileDialog



class FileHandlerEvent:
    @staticmethod
    def open_audio_directory(mainApp):
        # Method to open directory and extract audio folder path   
        directory_name = QFileDialog.getExistingDirectory(None, "Select Directory", "", QFileDialog.ShowDirsOnly)
        if directory_name:
            mainApp.lineEdit.setText(directory_name)
     
    @staticmethod
    def open_csv_directory(mainApp):
        # Method to open directory and extract CSV folder path 
        directory_name = QFileDialog.getExistingDirectory(None, "Select Directory", "", QFileDialog.ShowDirsOnly)
        if directory_name:
            mainApp.lineEdit.setText(directory_name)
    
    
    def open_files(self):
        pass

    
    





