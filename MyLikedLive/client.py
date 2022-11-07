# The main class and GUI/process handler
# Isaac Fisher

#TODO: nicer looking gui, colors/arrangements
#TODO: transition to songkick api when they start taking applications
#TODO: consider in-client error handling, but not too bad as is
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

# GUI Creation
class MainWindow(QMainWindow):
    # Initiates login process when login button is pressed
    def login(self):
        if os.path.exists(".cache"):
            os.remove(".cache")
        self.ss = SpotifyScraper()
        self.login_window.user_label.setText("You're logged in as: " + self.ss.get_username())
        self.login_window.continue_button.setEnabled(True)
        if not self.prompt_window == None:
            self.window_stack.removeWidget(self.prompt_window)
        self.prompt_window = self.make_prompt_window(QWidget())
        self.window_stack.insertWidget(1, self.prompt_window)


    # Moves to results page from prompt page
    def proceed_to_results(self):
        self.ss.find_artist_concerts()
        if not self.results_window == None:
            self.window_stack.removeWidget(self.results_window)
        self.results_window = self.make_results_window(QWidget())
        self.window_stack.insertWidget(2, self.results_window)
        self.window_stack.setCurrentIndex(2)

    # Changes the value stored in locationCode in resources/config.json
    def location_changed(self, location):
        settings.write_to_config("locationCode", dma_grabber.get_ids()[location])

    # Makes a generic QWidget into a login window
    def make_login_window(self, window):
        window.instruction_label = QLabel()
        window.instruction_label.setText("Press the button to connect to spotify")
        window.connect_button = QPushButton("Connect to spotify")
        window.connect_button.clicked.connect(self.login)
        window.user_label = QLabel()
        window.location_instructions = QLabel()
        window.location_instructions.setText("Choose your location:")
        window.location_dropdown = QComboBox()
        window.location_dropdown.addItems(loc for loc in dma_grabber.get_locations())
        window.location_dropdown.setCurrentText(dma_grabber.get_location(settings.get_location_code()))
        window.location_dropdown.currentTextChanged.connect(self.location_changed)
        window.continue_button = QPushButton("Continue")
        window.continue_button.setEnabled(False)
        window.continue_button.clicked.connect((lambda: self.window_stack.setCurrentIndex(1)))
        layout = QVBoxLayout()
        layout.addWidget(window.instruction_label)
        layout.addWidget(window.connect_button)
        layout.addWidget(window.user_label)
        layout.addWidget(window.location_instructions)
        layout.addWidget(window.location_dropdown)
        layout.addWidget(window.continue_button)
        window.setLayout(layout)
        return window

    # Makes a generic QWidget into a prompt window
    def make_prompt_window(self, window):
        recent_artists = "Lately, you've been listening to:\n" + ", ".join(self.ss.unique_artists)
        window.artist_label = QLabel(recent_artists)
        window.artist_label.setWordWrap(True)
        window.results_button = QPushButton("Get local concerts")
        window.results_button.clicked.connect(self.proceed_to_results)
        window.back_button = QPushButton("Back to login")
        window.back_button.clicked.connect((lambda: self.window_stack.setCurrentIndex(0)))
        layout = QVBoxLayout()
        layout.addWidget(window.artist_label)
        layout.addWidget(window.results_button)
        layout.addWidget(window.back_button)
        window.setLayout(layout)
        return window

    # Makes a generic QWidget into a results window
    def make_results_window(self, window):
        results = ""
        for concert_list in self.ss.all_concerts:
            results += str(concert_list) + "\n"
        window.concert_label = QLabel(results)
        window.back_button = QPushButton("Back to login")
        window.back_button.clicked.connect((lambda: self.window_stack.setCurrentIndex(0)))
        layout = QVBoxLayout()
        layout.addWidget(window.concert_label)
        layout.addWidget(window.back_button)
        window.setLayout(layout)
        return window

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Liked, Live")
        self.resize(QSize(100, 400))

        self.login_window = self.make_login_window(QWidget())
        self.prompt_window = None
        self.results_window = None

        self.window_stack = QStackedWidget()
        self.window_stack.addWidget(self.login_window)

        # If .cache exists, the user is already logged in
        if os.path.exists(".cache"):
            self.ss = SpotifyScraper()
            self.prompt_window = self.make_prompt_window(QWidget())
            self.window_stack.addWidget(self.prompt_window)
            self.window_stack.setCurrentIndex(1)
            self.login_window.user_label.setText("You're logged in as: " + self.ss.get_username())
            self.login_window.continue_button.setEnabled(True)
        else:
            self.window_stack.setCurrentIndex(0)

        self.setCentralWidget(self.window_stack)

if __name__ == "__main__":
    app = QApplication([])
    ex = MainWindow()
    ex.show()
    app.exec()
