import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from views.events.event_handler import EventHandler



class AudioRenameUI(QWidget):
    def file_inputs(self):
        self.setWindowTitle("Audio Rename")
        self.director_label = QLabel("Audio Directory", self)
        self.director_label.setGeometry(10, 50, 200, 30)

        # Input fiel
        self.dir_input = QLineEdit(self)
        self.dir_input.setGeometry(10, 75, 200, 30)

        self.audio_files_dir_selector = QPushButton("...", self)
        self.audio_files_dir_selector.setGeometry(210, 75, 30, 30)

        # Open Director
        self.event_handler = EventHandler()
        self.audio_files_dir_selector.clicked.connect(self.event_handler.open_directory)
        





