from spotify_scraper import SpotifyScraper
from utils import dma_grabber, settings
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QStackedWidget)
from PyQt6.QtCore import QSize
import os.path

class MainWindow(QMainWindow):
    # Initiates login process when login button is pressed
    def login(self):
        if os.path.exists(".cache"):
            os.remove(".cache")
        self.ss = SpotifyScraper()
        self.stack1.user_label.setText("You're logged in as: " + self.ss.get_username())
        self.stack1.continue_button.setEnabled(True)

    # Moves to results page from prompt page
    def proceed_to_results(self):
        self.ss.gather_recently_played()
        self.ss.find_artist_concerts()
        self.stack3 = self.make_results_window(QWidget())
        self.Stack.addWidget(self.stack3)
        self.Stack.setCurrentIndex(2)

    # Changes the value stored in locationCode in resources/config.json
    def location_changed(self, location):
        settings.write_to_config("locationCode", dma_grabber.get_ids()[location])

    # Makes a generic QWidget into a login window
    def make_login_window(self, stack):
        stack.instruction_label = QLabel()
        stack.instruction_label.setText("Press the button to connect to spotify")
        stack.connect_button = QPushButton("Connect to spotify")
        stack.connect_button.clicked.connect(self.login)
        stack.user_label = QLabel()
        stack.location_instructions = QLabel()
        stack.location_instructions.setText("Choose your location:")
        stack.location_dropdown = QComboBox()
        stack.location_dropdown.addItems(loc for loc in dma_grabber.get_locations())
        stack.location_dropdown.setCurrentText(dma_grabber.get_location(settings.get_location_code()))
        stack.location_dropdown.currentTextChanged.connect(self.location_changed)
        stack.continue_button = QPushButton("Continue")
        stack.continue_button.setEnabled(False)
        stack.continue_button.clicked.connect((lambda: self.Stack.setCurrentIndex(1)))
        layout = QVBoxLayout()
        layout.addWidget(stack.instruction_label)
        layout.addWidget(stack.connect_button)
        layout.addWidget(stack.user_label)
        layout.addWidget(stack.location_instructions)
        layout.addWidget(stack.location_dropdown)
        layout.addWidget(stack.continue_button)
        stack.setLayout(layout)
        return stack

    # Makes a generic QWidget into a prompt window
    def make_prompt_window(self, stack):
        stack.results_button = QPushButton("Get local concerts")
        stack.results_button.clicked.connect(self.proceed_to_results)
        stack.back_button = QPushButton("Back to login")
        stack.back_button.clicked.connect((lambda: self.Stack.setCurrentIndex(0)))
        layout = QVBoxLayout()
        layout.addWidget(stack.results_button)
        layout.addWidget(stack.back_button)
        stack.setLayout(layout)
        return stack

    # Makes a generic QWidget into a results window
    def make_results_window(self, stack):
        results = ""
        for concert_list in self.ss.all_concerts:
            results += str(concert_list) + "\n"
        stack.label = QLabel(results)
        layout = QVBoxLayout()
        layout.addWidget(stack.label)
        stack.setLayout(layout)
        return stack

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Liked, Live")

        self.stack1 = self.make_login_window(QWidget())
        self.stack2 = self.make_prompt_window(QWidget())

        self.Stack = QStackedWidget()
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)

        # If .cache exists, the user is already logged in
        if os.path.exists(".cache"):
            self.ss = SpotifyScraper()
            self.Stack.setCurrentIndex(1)
            self.stack1.user_label.setText("You're logged in as: " + self.ss.get_username())
            self.stack1.continue_button.setEnabled(True)
        else:
            self.Stack.setCurrentIndex(0)

        self.setCentralWidget(self.Stack)


app = QApplication([])
ex = MainWindow()
ex.show()
app.exec()

#print()
#print("Lately, you've been listening to: ")
#print(", ".join(ss.unique_artists))
#print()

#print("Searching for local concerts from these artists...\n")


#print("\n")
#for concert in ss.all_concerts:
#    print(concert)
#print()
