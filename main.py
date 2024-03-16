import os, sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from views.events.event_handler import FileHandlerEvent
from views.audio_rename_ui.generated_ui import Ui_SlimAudioFileRefactor

class AppWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Slim Audio File Refactor')
        self.mainAppUI = Ui_SlimAudioFileRefactor()
        self.mainAppUI.setupUi(self)
        self.select_dir_event()
        self.select_csv_dir_event()
    
    '''Selecting the button from designer and 
       connecting it to the event handler for audio directory'''
    def select_dir_event(self):
        self.event_handler = FileHandlerEvent()
        self.select_dir_btn = self.mainAppUI.pushButton
        self.select_dir_btn.clicked.connect(lambda: self.event_handler.open_audio_directory(self.mainAppUI))
    
    
    '''Selecting the button from designer and 
      connecting it to the event handler for csv directory'''
    def select_csv_dir_event(self):
        self.event_handler = FileHandlerEvent()
        self.select_csv_dir_btn = self.mainAppUI.pushButton_2
        self.select_csv_dir_btn.clicked.connect(lambda: self.event_handler.open_csv_directory(self.mainAppUI))
   






if __name__ == '__main__':
    app = QApplication(sys.argv);
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())



