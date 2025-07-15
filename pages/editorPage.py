from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit
from PyQt5.QtWidgets import QAction, QFileDialog, QTextEdit, QListWidgetItem, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize

from .imageEditorPopup import ImageEditorPopup
from .pageSettingPopup import PageSettingPopup
from core import convert2pdf

class EditorPage(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.initUI()

  def initUI(self):
    ### 레이아웃 ###
    ## 좌상단 레이아웃 - 썸네일 + 목록 ##
    self.layout_left = QVBoxLayout()
    self.image_list = QListWidget()
    self.image_list.setIconSize(QSize(80, 80))
    self.layout_left.addWidget(QLabel("이미지 목록"))
    self.layout_left.addWidget(self.image_list)

    ## 우상단 레이아웃 - 이미지 미리보기 ##
    self.layout_right = QVBoxLayout()
    self.preview_label = QLabel("이미지 미리보기")
    self.preview_label.setAlignment(Qt.AlignCenter)
    self.preview_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored) # QLabel이 조금씩 커지는 현상 방지
    self.layout_right.addWidget(QLabel("이미지 편집 화면"), stretch=1)
    self.layout_right.addWidget(self.preview_label, stretch=15)
    self.preview_label.setStyleSheet("border-style: solid;"
                                     "border-width: 2px;"
                                     "border-color: #FFFFFF")
    
    ## 하단 레이아웃 - 버튼 ##
    self.layout_bottom = QHBoxLayout()
    self.btn_openImg = QPushButton("이미지 열기")
    self.btn_editImg = QPushButton("이미지 편집")
    self.btn_pageSetting = QPushButton("페이지 설정")
    self.btn_save = QPushButton("PDF로 저장")
    self.layout_bottom.addWidget(self.btn_openImg)
    self.layout_bottom.addWidget(self.btn_editImg)
    self.layout_bottom.addWidget(self.btn_pageSetting)
    self.layout_bottom.addWidget(self.btn_save)

    top_layout = QHBoxLayout()
    top_layout.addLayout(self.layout_left, stretch=1)
    top_layout.addLayout(self.layout_right, stretch=3)

    main_layout = QVBoxLayout()
    main_layout.addLayout(top_layout)
    main_layout.addLayout(self.layout_bottom)
    
    self.setLayout(main_layout)

    ### 이벤트 처리 ###
    self.btn_openImg.clicked.connect(self.showFileDialog)
    self.btn_editImg.clicked.connect(self.openImageEditor)
    self.btn_pageSetting.clicked.connect(self.openPageSetting)
    self.btn_save.clicked.connect(self.createPDFfile)

    self.image_list.itemClicked.connect(self.changeDisplay)

    self.image_paths = []

    ##############  PDF 변환 위해 넘겨야 하는 자료(로직 추가 필요) ##################
    img_sources = []  # img_sources의 element 구조: [path, x1, y1, x2, y2] (비율로 받음)
    padding = []      # padding의 element 구조    : [좌측, 상단, 우측, 하단]
    ###########################################################################

  def showFileDialog(self):
    files, _ = QFileDialog.getOpenFileNames(self, '이미지 파일 선택', './', 'Image Files (*.png *.jpg *.bmp)')
    for file_path in files:
      self.image_paths.append(file_path)

      pixmap = QPixmap(file_path)
      icon = QIcon(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))

      item = QListWidgetItem(icon, file_path.split('/')[-1])
      item.setData(Qt.UserRole, file_path)
      self.image_list.addItem(item)

      if self.image_list.count() == 1:
        self.displayImage(file_path)

  def openImageEditor(self):
    currentItem = self.image_list.currentItem()
    if currentItem:
      image_path = currentItem.data(Qt.UserRole)
      editor = ImageEditorPopup(image_path, self)
      editor.exec_()

  def openPageSetting(self):
    pageSetting = PageSettingPopup(self)
    pageSetting.exec_()

  def createPDFfile(self):
    return 0  

  ### 이미지 미리보기 ###
  def displayImage(self, image_path):
    pixmap = QPixmap(image_path)
    scaled_pixmap = pixmap.scaled(self.preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    self.preview_label.setPixmap(scaled_pixmap)

  def changeDisplay(self, item):
    index = self.image_list.row(item)
    pixmap = QPixmap(self.image_paths[index])
    scaled_pixmap = pixmap.scaled(self.preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    self.preview_label.setPixmap(scaled_pixmap)