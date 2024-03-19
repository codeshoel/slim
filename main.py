import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import shutil
import pandas as pd
from datetime import datetime
import random


basedir = os.path.dirname(__file__)


class CustomMessageBox(QMessageBox):
    def event(self, e):
        if e.type() == QEvent.Close:
            if self.clickedButton() == self.defaultButton():
                self.show_matched_files_slot()
        return super().event(e)


class WorkerThread(QThread):
    task_finished = pyqtSignal(dict)
    task_progress = pyqtSignal(int)

    def __init__(self, directory, file_path, prefix):
        super().__init__()
        self.directory = directory
        self.file_path = file_path
        self.prefix = prefix
        self.cancelled = False

    def run(self):
        try:
            output_folder = os.path.join(self.directory, "Renamed_Files")
            os.makedirs(output_folder, exist_ok=True)

            def get_excel_calls():
                df = pd.read_excel(self.file_path)
                df['PhoneNumber'] = df['PhoneNumber'].astype(str).str.split('.').str[0]
                df['PhoneNumber'] = df['PhoneNumber'].apply(lambda x: '0' + x[3:] if x.startswith('234') else x)
                return df[['Id', 'PhoneNumber']]

            def get_audio_files():
                audio_files = []
                for filename in os.listdir(self.directory):
                    if filename.endswith(".mp3"):
                        _path = os.path.join(self.directory, filename)
                        _file_name = os.path.splitext(filename)[0]
                        _date = datetime.strptime(_file_name.split('T')[0], '%Y%m%d').strftime('%d%m%y')
                        _phone = str(_file_name.split('_')[2])
                        if _phone.startswith('234'):
                            _phone = '0' + _phone[3:]
                        audio_files.append((_path, _date, _phone))
                return audio_files

            def rename_file(call, _id):
                tag = random.randint(1, 20)
                path, date, phone = call
                new_path = os.path.join(output_folder, f'{self.prefix}_{_id}_{date}.mp3')
                if os.path.exists(new_path):
                    new_path = os.path.join(output_folder, f'{self.prefix}_{_id}_{date}_{tag}.mp3')
                shutil.copyfile(path, new_path, follow_symlinks=True)

            # Get data from Excel file and audio files
            excel_calls = get_excel_calls()
            audio_files = get_audio_files()

            # Rename audio files based on matching criteria
            i = 0
            matched = []
            total_files = len(audio_files)
            for idx, call_row in enumerate(audio_files):
                if self.cancelled:
                    return
                for _, excel_row in excel_calls.iterrows():
                    if call_row[2] == excel_row['PhoneNumber']:
                        matched.append([call_row[2], excel_row['Id']])
                        i += 1
                        rename_file(call_row, excel_row['Id'])
                progress = (idx + 1) * 100 // total_files
                self.task_progress.emit(progress)

            # Return information about the renaming process
            message = f'{i} calls were successfully renamed' if i > 0 else 'No calls were found to be renamed'
            dict_msg = {'renamed_path': output_folder, 'message': message, 'matched_files': matched}
            self.task_finished.emit(dict_msg)

        except Exception as e:
            # Handle any specific exceptions here, or simply print the error message
            print(f"An error occurred: {e}")

    def cancel(self):
        self.cancelled = True

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        try:
            with open(os.path.join(basedir, 'static/css/style.css'), 'r') as f:
                # initializing stylesheet
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Stylesheet file 'style.css' not found in 'static' directory.")

        # Constants
        self.warningAlert = "Warning Alert"
        self.successAlert = "Success Alert"


        self.setWindowTitle("Slim tools")
        self.setWindowIcon(QIcon(os.path.join(basedir, 'static/images/icon.png')))
        self.setGeometry(0, 0, 300, 300)
        self.setObjectName("mainWindow")
        self.center()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Tab widgets
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.currentChanged.connect(self.on_tab_changed)  # Connect the signal to slot

        # Add tabs
        self.tab1 = QWidget()
        self.tab1.setObjectName("rename_audio_tab")
        self.tab1_layout = QVBoxLayout()
        self.tab1_layout.addWidget(self.file_inputs())
        self.tab1.setLayout(self.tab1_layout)

        # tab2
        self.tab2 = QWidget()
        self.tab2_layout = QVBoxLayout()
        self.tab2_layout.addWidget(self.second_tab())
        self.tab2.setLayout(self.tab2_layout)

        # Add tabs to the tab widget
        self.tabs.addTab(self.tab1, 'Rename Audio')
        self.tabs.addTab(self.tab2, 'Audio Overlay')

        # Add the tab widget to the main layout
        self.layout.addWidget(self.tabs)

    def on_tab_changed(self, index):
        if index == 0:
            self.tab1.show()
            self.tab2.hide()
        elif index == 1:
            self.tab1.hide()
            self.tab2.show()

    def file_inputs(self):
        widget = QWidget(self)
        layout = QGridLayout(widget)

        self.dir_input = QLineEdit()
        self.dir_input.setPlaceholderText("Select audio location")
        self.dir_input.setObjectName("dir_input")
        self.dir_input.setReadOnly(True)

        self.audio_files_dir_selector_bnt = QPushButton("...")
        self.audio_files_dir_selector_bnt.setObjectName("open_dir_btn")

        self.file_dir_input = QLineEdit()
        self.file_dir_input.setPlaceholderText("Select csv file")
        self.file_dir_input.setObjectName("select_csv_input")
        self.file_dir_input.setReadOnly(True)

        self.csv_files_dir_selector_btn = QPushButton("...")
        self.csv_files_dir_selector_btn.setObjectName("select_file_btn")

        self.preFix = QLineEdit()
        self.preFix.setObjectName("prefix_input")
        self.preFix.setPlaceholderText("Enter prefix")
        self.preFix.setText("NIG")
        
        self.renameButton = QPushButton("Rename")
        self.renameButton.setObjectName("rename_btn")

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setObjectName("cancel_btn")
        self.cancelButton.hide()  # Initially hide the cancel button

        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()  # Initially hide the progress bar

        layout.addWidget(self.dir_input, 0, 0)
        layout.addWidget(self.audio_files_dir_selector_bnt, 0, 1)
        layout.addWidget(self.file_dir_input, 1, 0)
        layout.addWidget(self.csv_files_dir_selector_btn, 1, 1)
        layout.addWidget(self.preFix, 2, 0)
        layout.addWidget(self.renameButton, 3, 0)
        layout.addWidget(self.cancelButton, 3, 1)
        layout.addWidget(self.progress_bar, 4, 0, 1, 2)

        # Event handlers
        self.audio_files_dir_selector_bnt.clicked.connect(self.open_directory)
        self.csv_files_dir_selector_btn.clicked.connect(self.open_csv_file)
        # self.renameButton.clicked.connect(self.popup_widget)
        self.renameButton.clicked.connect(self.rename_audio_files)
        self.cancelButton.clicked.connect(self.cancel_task)

        widget.setContentsMargins(30, 30, 30, 0)
        widget.setFixedSize(300, 300)

        return widget

    def open_directory(self):
        try:
            options = QFileDialog.ShowDirsOnly
            dir_name = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', options)
            if dir_name:
                self.dir_input.setText(dir_name)
        except Exception as e:
            # Handle any specific exceptions here, or simply print the error message
            print(f"An error occurred: {e}")

    def open_csv_file(self):
        try:
            options = QFileDialog.Options()
            file_formats = "CSV Files (*.csv *.xlsx);;All Files (*)"
            file_name, _ = QFileDialog.getOpenFileName(self, "Select a file", "", file_formats, options=options)
            if file_name:
                self.file_dir_input.setText(file_name)
        except Exception as e:
            # Handle any specific exceptions here, or simply print the error message
            print(f"An error occurred: {e}")

    def rename_audio_files(self):
        directory = self.dir_input.text()
        file_path = self.file_dir_input.text()
        prefix = self.preFix.text()

        if not directory or not file_path:
            self.requirementAlert = QMessageBox()
            self.requirementLabel = "Please select required directory and file to proceed"
            self.requirementAlert.setIcon(QMessageBox.Warning)  # Corrected line
            self.requirementAlert.about(None, self.warningAlert, self.requirementLabel)
            return


        # Show the progress bar and cancel button
        self.progress_bar.show()
        self.cancelButton.show()

        # Start the worker thread
        self.worker_thread = WorkerThread(directory, file_path, prefix)
        self.worker_thread.task_finished.connect(self.show_alert)
        self.worker_thread.task_progress.connect(self.update_progress)
        self.worker_thread.start()

    def show_alert(self, dict_msg):

        # Hide the progress bar and cancel button
        self.progress_bar.hide()
        self.cancelButton.hide()

        # Create CustomMessageBox for the summary message
        show_table_button = QPushButton("Show Matched Files")
        self.alertMessage = CustomMessageBox()
        self.alertMessage.setGeometry(0, 0, 400, 400)
        self.alertMessage.setWindowTitle("Task Summary")
        self.alertMessage.setIcon(QMessageBox.Information)
        self.alertMessage.setDefaultButton(show_table_button)
        self.alertMessage.setInformativeText("Click OK to view matched files.")
        # Create layout for the QMessageBox
        alert_layout = QVBoxLayout()

        if dict_msg['matched_files']:
            table_button_layout = QHBoxLayout()

            # Create a button to show matched files in a table
            show_table_button.clicked.connect(self.show_matched_files_slot)
            table_button_layout.addWidget(show_table_button)

            alert_layout.addLayout(table_button_layout)

            alert_layout.setSizeConstraint(QLayout.SetMinimumSize)

        self.alertMessage.setLayout(alert_layout)
        self.alertMessage.resize(600, 400)

        self.alertMessage.exec_()

    def show_matched_files_slot(self):
        # Create QWidget for displaying the matched files in a table
        matched_files_widget = QWidget()
        matched_files_widget.setWindowTitle("Matched Files")
        matched_files_widget.resize(600, 400)

        # Create layout for the QWidget
        matched_files_layout = QVBoxLayout(matched_files_widget)

        # Create QTableWidget to display matched files
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Phone Number", "ID"])
        table.setRowCount(len(self.matched_files))

        for i, (phone_number, _id) in enumerate(self.matched_files):
            table.setItem(i, 0, QTableWidgetItem(phone_number))
            table.setItem(i, 1, QTableWidgetItem(str(_id)))

        matched_files_layout.addWidget(table)

        # Show the QWidget containing the matched files table
        matched_files_widget.show()





    def cancel_task(self):
        if hasattr(self, 'worker_thread') and self.worker_thread.isRunning():
            self.worker_thread.cancel()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)


    def second_tab(self):
        widget = QWidget(self)
        layout = QVBoxLayout(widget)

        self.label = QLabel()
        self.label.setGeometry(0, 0, 0, 0)
        self.label.setText("Coming Soon..!")
        self.label.setObjectName("coming_soon")

        layout.addWidget(self.label)

        return widget
    # def popup_widget(self):
    #     layout = QVBoxLayout()
    #     layout.addWidget(QPushButton("Hello Gabriel"))
    #     layout.exec_()

    def center(self):
        # Get the screen resolution and set the position of the application
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) / 2
        y = (screen.height() - size.height()) / 2
        self.move(int(x), int(y))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
