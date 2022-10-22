from spotify_scraper import SpotifyScraper
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QListWidget, QStackedWidget, QFormLayout, QLineEdit, QHBoxLayout, QRadioButton, QCheckBox
from PyQt6.QtCore import QSize
import os.path

class MainWindow(QMainWindow):
    def login(self):
        if os.path.exists(".cache"):
            os.remove(".cache")
        self.ss = SpotifyScraper()
        self.Stack.setCurrentIndex(1)


    def make_login_window(self, stack):
        stack.instruction_label = QLabel()
        stack.instruction_label.setText("Press the button to connect to spotify")
        stack.connect_button = QPushButton("Connect to spotify")
        stack.connect_button.clicked.connect(self.login)
        layout = QVBoxLayout()
        layout.addWidget(stack.instruction_label)
        layout.addWidget(stack.connect_button)
        stack.setLayout(layout)
        return stack

    def make_prompt_window(self, stack):
        layout = QVBoxLayout()
        stack.label = QLabel("Another Window")
        layout.addWidget(stack.label)
        stack.setLayout(layout)
        return stack

    def make_results_window(self, stack):
        layout = QVBoxLayout()
        stack.label = QLabel("Another Window")
        layout.addWidget(stack.label)
        stack.setLayout(layout)
        return stack

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Liked, Live")
        self.resize(QSize(400, 400))

        self.stack1 = self.make_login_window(QWidget())
        self.stack2 = self.make_prompt_window(QWidget())
        self.stack3 = self.make_results_window(QWidget())

        self.Stack = QStackedWidget()
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)

        if os.path.exists(".cache"):
            self.Stack.setCurrentIndex(1)
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
