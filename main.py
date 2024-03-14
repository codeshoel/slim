import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from views.audio_rename_ui.ui import AudioRenameUI



class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple App")
        self.setGeometry(50, 50, 500, 300)
        # AudioRenameUI.file_inputs(self)

        self.central_widge = QWidget(self)
        self.setCentralWidget(self.central_widge);

        self.layout = QVBoxLayout(self.central_widge)

        # Tab widgets
        self.tabs = QTabWidget(self)

        # Add tabs
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        # Add widgets to each of the tabs

        # tab1
        self.tab1.layout = QVBoxLayout()
        
        self.tab1.layout.addWidget(AudioRenameUI.file_inputs(self))
        self.tab1.setLayout(self.tab1.layout)

        # tab2
        self.tab2.layout = QVBoxLayout()
        self.tab2.layout.addWidget(QPushButton('Button 2 on Tab 2'))
        self.tab2.setLayout(self.tab2.layout)

        # Add tabs to the tab widget
        self.tabs.addTab(self.tab1, 'Rename Audio Files')
        self.tabs.addTab(self.tab2, 'Tab 2')

        # Add the tab widget to the main layout
        self.layout.addWidget(self.tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv);
    window = Window()
    window.show()
    sys.exit(app.exec())
