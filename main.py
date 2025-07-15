import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QAction, QDesktopWidget, qApp, QWidget
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout
from PyQt5.QtGui import QIcon

from pages.mainPage import MainPage
from pages.setupPage import SetupPage
from pages.editorPage import EditorPage

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("PDFConverter")
    self.setWindowIcon(QIcon('pdfConverter/assets/img/icon.jpg'))
    self.resize(1000, 750)
    self.center()

    self.initUI()
    self.setupLayout()
    self.setupSignals()

    self.stack.setCurrentIndex(0)
  
  def initUI(self):
    ## 메뉴바 ##
    menubar = self.menuBar()
    menubar.setNativeMenuBar(False)
    filemenu = menubar.addMenu('&File')
    editmenu = menubar.addMenu('&Edit')
    settingmenu = menubar.addMenu('&Settings')
    infomenu = menubar.addMenu('&Info')

    self.action_main = QAction("Main Page", self)
    self.action_setup = QAction("Setup Page", self)
    self.action_editor = QAction("Editor Page", self)

    editmenu.addAction(self.action_editor)

    settingmenu.addAction(self.action_main)
    settingmenu.addAction(self.action_setup)

    self.main_page = MainPage()
    self.setup_page = SetupPage()
    self.editor_page = EditorPage()

    self.stack = QStackedWidget()
    self.stack.addWidget(self.main_page) # index 0
    self.stack.addWidget(self.setup_page) # index 1
    self.stack.addWidget(self.editor_page) # index 2

  def setupLayout(self):
    central_widget = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(self.stack)
    central_widget.setLayout(layout)
    self.setCentralWidget(central_widget)

  def setupSignals(self):
    self.action_main.triggered.connect(lambda: self.stack.setCurrentIndex(0))
    self.action_setup.triggered.connect(lambda: self.stack.setCurrentIndex(1))
    self.action_editor.triggered.connect(lambda: self.stack.setCurrentIndex(2))

  def center(self):
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())