import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QAction, QDesktopWidget, qApp
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class SetupPage(QWidget):
  def __init__(self):
    super().__init__()
    label = QLabel("설정 페이지입니다")
    label.setAlignment(Qt.AlignCenter)

    layout = QVBoxLayout()
    layout.addWidget(label)
    self.setLayout(layout)