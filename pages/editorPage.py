import os

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit
from PyQt5.QtWidgets import QAction, QFileDialog, QTextEdit, QListWidgetItem, QSizePolicy, QDialog, QSlider
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QSize

from .imageEditorPopup import ImageEditorPopup
from .pageSettingPopup import PageSettingPopup
from core.convert2pdf import convert2PDF

class EditorPage(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.initUI()

  def initUI(self):
    ### 필요한 데이터 / 변수 ###
    self.pageSize = None
    self.pageRatio = 1
    self.pageMargin = 0

    self.original_pixmap = None # 현재 미리보기에서 보이는 이미지의 원본

    #########################
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
    self.btn_adjustImg = QPushButton("이미지를 페이지 크기에 맞춤")
    self.layout_right.addWidget(self.btn_adjustImg, stretch=1)
    # 이미지 크기 조절 슬라이더 #
    self.slider = QSlider(Qt.Horizontal)
    self.slider.setMinimum(10)
    self.slider.setMaximum(200)
    self.slider.setValue(100)
    self.slider.setTickPosition(QSlider.TicksBelow)
    self.slider.setTickInterval(10)
    self.layout_right.addWidget(self.slider, stretch = 1)
    
    self.layout_right.addWidget(self.preview_label, stretch=15)
    self.preview_label.setStyleSheet("border-style: solid;"
                                     "border-width: 2px;"
                                     "border-color: #FFFFFF;"
                                     "background-color: lightblue;")
    
    self.previewImg_label = QLabel("실제 이미지", self.preview_label)
    self.previewImg_label.setStyleSheet("background-color: transparent;"
                                        "border-style: solid;"
                                        "border-width: 2px;"
                                        "border-color: red;")
    self.previewImg_label.setAlignment(Qt.AlignCenter)
    
    
    ## 하단 레이아웃 - 버튼 ##
    self.layout_bottom = QHBoxLayout()
    self.btn_openImg = QPushButton("이미지 열기")
    self.btn_editImg = QPushButton("이미지 편집")
    self.btn_savePreview = QPushButton("미리보기 저장")
    self.btn_pageSetting = QPushButton("페이지 설정")
    self.btn_save = QPushButton("PDF로 저장")
    self.layout_bottom.addWidget(self.btn_openImg)
    self.layout_bottom.addWidget(self.btn_editImg)
    self.layout_bottom.addWidget(self.btn_savePreview)
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
    self.preview_index = 0

    self.btn_adjustImg.clicked.connect(self.adjustImgtoPage)
    self.slider.valueChanged.connect(self.scalePreviewImg)

    self.btn_openImg.clicked.connect(self.showFileDialog)
    self.btn_editImg.clicked.connect(self.openImageEditor)
    self.btn_savePreview.clicked.connect(self.savePreview)
    self.btn_pageSetting.clicked.connect(self.openPageSetting)
    self.btn_save.clicked.connect(self.createPDFfile)

    self.image_list.itemClicked.connect(self.changeDisplay)

    self.image_paths = []

    ##############  PDF 변환 위해 넘겨야 하는 자료(로직 추가 필요) ##################
    self.img_sources = []  # img_sources의 element 구조: [path, x1, y1, x2, y2] (비율로 받음)
    self.padding = []      # padding의 element 구조    : [좌측, 상단, 우측, 하단]
    ###########################################################################

  def showFileDialog(self):
    files, _ = QFileDialog.getOpenFileNames(self, '이미지 파일 선택', './', 'Image Files (*.png *.jpg *.bmp)')
    for file_path in files:
      self.image_paths.append(file_path)
      # self.img_sources.append([file_path, 0 for _ in range(4)])

      pixmap = QPixmap(file_path)
      icon = QIcon(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))

      item = QListWidgetItem(icon, file_path.split('/')[-1])
      item.setData(Qt.UserRole, file_path)
      self.image_list.addItem(item)

      if self.image_list.count() == 1:
        self.displayImage(file_path)

  ### 미리보기 이미지를 페이지 크기에 채움
  def adjustImgtoPage(self):
    pixmap = self.preview_label.pixmap()
    if pixmap:
      width = pixmap.width()
      height = pixmap.height()
      if height / width > self.pageRatio: #가로여백이 남을때
        new_scale = height / self.previewImg_label.height()
      else: # 세로 여백이 남을때
        new_scale = width / self.previewImg_label.width()
      new_size = QSize(int(width / new_scale), int(height / new_scale))
      scaled_pixmap = pixmap.scaled(new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
      self.preview_label.setPixmap(scaled_pixmap)

  def scalePreviewImg(self, value):
    factor = value / 100
    pixmap = self.original_pixmap
    if pixmap:
      new_size = pixmap.size() * factor
      scaled_pixmap = pixmap.scaled(new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
      self.preview_label.setPixmap(scaled_pixmap)

  def openImageEditor(self):
    currentItem = self.image_list.currentItem()
    if currentItem:
      image_path = currentItem.data(Qt.UserRole)
      editor = ImageEditorPopup(image_path, self)
      if editor.exec_() == QDialog.Accepted:
        cropped_pixmap = editor.cropped_pixmap
        self.preview_label.setPixmap(cropped_pixmap)
        self.original_pixmap = cropped_pixmap

  ### 미리보기 저장 ###
  def savePreview(self):
    index = self.preview_index
    file_name = os.path.basename(self.image_paths[index])
    name, _ = os.path.splitext(file_name)
    pixmap = self.preview_label.pixmap()
    if not pixmap:
      return
    save_folder = QFileDialog.getExistingDirectory(self, "저장할 폴더 선택","./")
    if save_folder:
      save_path = os.path.join(save_folder, f"{name}_cropped.png")

      ##### 설정한 페이지 크기보다 이미지가 작은 경우 사용자가 설정한 단색으로 여백 채우기 #####
      img_width = pixmap.width()
      img_height = pixmap.height()
      new_width = self.previewImg_label.width()
      new_height = self.previewImg_label.height()

      if img_width < new_width or img_height < new_height:
        margin_width = (new_width - img_width) // 2
        margin_height = (new_height - img_height) // 2

        new_pixmap = QPixmap(new_width, new_height)
        new_pixmap.fill(QColor("black"))

        painter = QPainter(new_pixmap)
        painter.drawPixmap(margin_width, margin_height, pixmap)
        painter.end()
        pixmap = new_pixmap

      pixmap.save(save_path, "PNG")
  
  ### 페이지 설정 관련 ###
  def openPageSetting(self):
    pageSetting = PageSettingPopup(self)
    pageSetting.sig_pageSettingConfirmed.connect(self.applyPageSettings) # 팝업창에서 정보를 받음
    pageSetting.exec_()
  def applyPageSettings(self, settings):
    self.pageSize = settings["pageSize"]
    self.updatePreviewGeometry()

  def createPDFfile(self):
    convert2PDF(self.img_sources, [], pdf_path='C:\\GIST\\dev\\pdfConverter\\ouput.pdf') ### 임시, 꼭 크롭한 이미지 파일이 들어가도록 수정!!! 

  ### 이미지 미리보기 ###
  def displayImage(self, image_path):
    pixmap = QPixmap(image_path)
    scaled_pixmap = pixmap.scaled(self.preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    self.preview_label.setPixmap(scaled_pixmap)

  def changeDisplay(self, item):
    index = self.image_list.row(item)
    self.preview_index = index
    pixmap = QPixmap(self.image_paths[index])
    self.original_pixmap = pixmap
    # scaled_pixmap = pixmap.scaled(self.preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    self.preview_label.setPixmap(self.original_pixmap)

  ### 창의 크기가 변경될 때 ###
  def resizeEvent(self, event):
    super().resizeEvent(event)
    self.updatePreviewGeometry()

  def updatePreviewGeometry(self):
    preview_width = self.preview_label.width()
    preview_height = self.preview_label.height()

    if self.pageSize == "A4":
      self.pageRatio = 1.414
    child_height = preview_height
    child_width = int(child_height / self.pageRatio) ### 페이지 크기 설정에 따라 유동적으로 바뀌어야 함
    x = (preview_width - child_width) // 2
    y = 0

    self.previewImg_label.setGeometry(x, y, child_width, child_height)
