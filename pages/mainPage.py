import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QAction, QDesktopWidget, qApp, QWidget
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class MainPage(QWidget):
  def __init__(self):
    super().__init__()
    label = QLabel("메인 페이지입니다")
    label.setAlignment(Qt.AlignCenter)

    layout = QVBoxLayout()
    layout.addWidget(label)
    self.setLayout(layout)