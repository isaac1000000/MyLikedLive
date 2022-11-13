# The main class and GUI/process handler

#TODO: transition to songkick api when they start taking applications
#TODO: consider in-client error handling, but not too bad as is
from spotify_scraper import SpotifyScraper
from utils import dma_grabber, settings, gui_tools
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QComboBox,
    QGridLayout,
    QWidget,
    QSpacerItem,
    QPushButton,
    QStackedWidget)
from PyQt6.QtCore import Qt, QSize
import os.path

# GUI Creation
class MainWindow(QMainWindow):
    # Initiates login process when login button is pressed
    def login(self):
        if os.path.exists(".cache"):
            os.remove(".cache")
        self.ss = SpotifyScraper()
        self.login_window.user_label.setText(">>> You're logged in as: " + self.ss.get_username())
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
        window.greeting_label = QLabel()
        window.greeting_label.setText(">>> Your Liked, Live")
        window.greeting_label.setStyleSheet("font-weight: bold; font-size: 25px")
        window.connect_button = QPushButton("[Connect to Spotify]")
        window.connect_button.clicked.connect(self.login)
        window.user_label = QLabel()
        window.location_dropdown = QComboBox()
        window.location_dropdown.addItems(loc for loc in dma_grabber.get_locations())
        window.location_dropdown.setCurrentText(dma_grabber.get_location(settings.get_location_code()))
        window.location_dropdown.currentTextChanged.connect(self.location_changed)
        window.location_dropdown.setFixedWidth(275)
        window.continue_button = QPushButton("[Continue]")
        window.continue_button.setEnabled(False)
        window.continue_button.clicked.connect((lambda: self.window_stack.setCurrentIndex(1)))
        layout = QGridLayout()
        layout.addWidget(window.greeting_label, 0, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(window.connect_button, 1, 1)
        layout.addWidget(window.user_label, 1, 2)
        layout.addWidget(window.location_dropdown, 2, 0, 1, 2)
        layout.addWidget(window.continue_button, 2, 2)
        window.setLayout(layout)
        return window

    # Makes a generic QWidget into a prompt window
    def make_prompt_window(self, window):
        recent_artists = "Lately, you've been listening to:\n" + gui_tools.list_styling(self.ss.unique_artists)
        window.artist_label = QLabel(recent_artists)
        window.artist_label.setWordWrap(True)
        window.results_button = QPushButton("[Get local concerts]")
        window.results_button.clicked.connect(self.proceed_to_results)
        window.back_button = QPushButton("[Back to login]")
        window.back_button.clicked.connect((lambda: self.window_stack.setCurrentIndex(0)))
        layout = QGridLayout()
        layout.addWidget(window.artist_label, 0, 0, 1, 0)
        layout.addWidget(window.results_button, 1, 1)
        layout.addWidget(window.back_button, 1, 0)
        window.setLayout(layout)
        return window

    # Makes a generic QWidget into a results window
    def make_results_window(self, window):
        results = gui_tools.list_styling(self.ss.all_concerts)
        window.concert_label = QLabel(results)
        window.back_button = QPushButton("[Back to login]")
        window.back_button.clicked.connect((lambda: self.window_stack.setCurrentIndex(0)))
        layout = QGridLayout()
        layout.addWidget(window.concert_label, 0, 0, 2, 0)
        layout.addWidget(QLabel(), 1, 1)
        layout.addWidget(window.back_button, 1, 0)
        window.setLayout(layout)
        return window

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Liked, Live")
        self.resize(QSize(480, 400))

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
            self.login_window.user_label.setText(">>> Logged in as: " + self.ss.get_username()[:10])
            self.login_window.continue_button.setEnabled(True)
        else:
            self.window_stack.setCurrentIndex(0)

        self.setCentralWidget(self.window_stack)

if __name__ == "__main__":
    app = QApplication([])
    ex = MainWindow()

    app.setStyleSheet("""
    QWidget {
        background-color: "black";
        color: "green";
    }
    QComboBox {
        border: 1px solid green;
    }
    QPushButton {
        border: .5px solid green;
    }
    """)

    ex.show()
    app.exec()
