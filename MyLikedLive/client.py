from spotify_scraper import SpotifyScraper
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import QSize
import os.path

class LoginWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Liked, Live")
        self.resize(QSize(400, 400))

        self.instruction_label = QLabel()
        self.instruction_label.setText("Press the button to connect to spotify")

        self.connect_button = QPushButton("Connect to spotify")
        self.connect_button.clicked.connect(self.login)
        self.connect_button.clicked.connect(self.new_window)

        layout = QVBoxLayout()
        layout.addWidget(self.instruction_label)
        layout.addWidget(self.connect_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def login(self):
        if os.path.exists(".cache"):
            os.remove(".cache")
        self.ss = SpotifyScraper()

    def new_window(self, checked):
        self.prompt_window = PromptWindow()
        self.prompt_window.show()

class PromptWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)

app = QApplication([])
login_window = LoginWindow()
login_window.show()
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
