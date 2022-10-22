from spotify_scraper import SpotifyScraper
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QListWidget, QStackedWidget, QFormLayout, QLineEdit, QHBoxLayout, QRadioButton, QCheckBox
from PyQt6.QtCore import QSize
import os.path

class MainWindow(QMainWindow):
    #TODO: use stackedwidget to better handle multiple windows
    def login(self):
        if os.path.exists(".cache"):
            os.remove(".cache")
        self.ss = SpotifyScraper()


    def make_login_window(self, stack):
        stack.setWindowTitle("My Liked, Live")
        stack.resize(QSize(400, 400))

        stack.instruction_label = QLabel()
        stack.instruction_label.setText("Press the button to connect to spotify")

        stack.connect_button = QPushButton("Connect to spotify")
        stack.connect_button.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(stack.instruction_label)
        layout.addWidget(stack.connect_button)

        stack.setLayout(layout)

    def make_prompt_window(self, stack):
        layout = QVBoxLayout()
        stack.label = QLabel("Another Window")
        layout.addWidget(stack.label)
        stack.setLayout(layout)

    def make_result_window(self, stack):
        layout = QVBoxLayout()
        stack.label = QLabel("Another Window")
        layout.addWidget(stack.label)
        stack.setLayout(layout)


    def __init__(self):
      super(MainWindow, self).__init__()
      self.leftlist = QListWidget()
      self.leftlist.insertItem (0, 'login_window' )
      self.leftlist.insertItem (1, 'prompt_window' )
      self.leftlist.insertItem (2, 'results_window' )

      self.stack1 = self.make_login_window(QWidget())
      self.stack2 = self.make_prompt_window(QWidget())
      self.stack3 = self.make_result_window(QWidget())


      self.Stack = QStackedWidget()
      self.Stack.addWidget(self.stack1)
      self.Stack.addWidget(self.stack2)
      self.Stack.addWidget(self.stack3)

      layout = QVBoxLayout()
      layout.addWidget(Stack)

      self.show()

#app = QApplication([])
#login_window = LoginWindow()
#login_window.show()
#app.exec()

#print()
#print("Lately, you've been listening to: ")
#print(", ".join(ss.unique_artists))
#print()

#print("Searching for local concerts from these artists...\n")


#print("\n")
#for concert in ss.all_concerts:
#    print(concert)
#print()


class stackedExample(QWidget):

   def __init__(self):
      super(stackedExample, self).__init__()
      self.leftlist = QListWidget()
      self.leftlist.insertItem (0, 'Contact' )
      self.leftlist.insertItem (1, 'Personal' )
      self.leftlist.insertItem (2, 'Educational' )

      self.stack1 = QWidget()
      self.stack2 = QWidget()
      self.stack3 = QWidget()

      self.stack1UI()
      self.stack2UI()
      self.stack3UI()

      self.Stack = QStackedWidget(self)
      self.Stack.addWidget(self.stack1)
      self.Stack.addWidget(self.stack2)
      self.Stack.addWidget(self.stack3)

      hbox = QHBoxLayout(self)
      hbox.addWidget(self.leftlist)
      hbox.addWidget(self.Stack)

      self.setLayout(hbox)
      self.leftlist.currentRowChanged.connect(self.display)
      self.setGeometry(300, 50, 10,10)
      self.setWindowTitle('StackedWidget demo')
      self.show()

   def stack1UI(self):
      layout = QFormLayout()
      layout.addRow("Name",QLineEdit())
      layout.addRow("Address",QLineEdit())
      #self.setTabText(0,"Contact Details")
      self.stack1.setLayout(layout)

   def stack2UI(self):
      layout = QFormLayout()
      sex = QHBoxLayout()
      sex.addWidget(QRadioButton("Male"))
      sex.addWidget(QRadioButton("Female"))
      layout.addRow(QLabel("Sex"),sex)
      layout.addRow("Date of Birth",QLineEdit())

      self.stack2.setLayout(layout)

   def stack3UI(self):
      layout = QHBoxLayout()
      layout.addWidget(QLabel("subjects"))
      layout.addWidget(QCheckBox("Physics"))
      layout.addWidget(QCheckBox("Maths"))
      self.stack3.setLayout(layout)

   def display(self,i):
      self.Stack.setCurrentIndex(i)


app = QApplication([])
ex = MainWindow()
app.exec()
