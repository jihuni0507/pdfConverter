from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QDialog, QComboBox, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtCore import Qt

class PageSettingPopup(QDialog):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setWindowTitle("페이지 설정")
    self.setMinimumSize(300, 600)
    self.initUI()

  def initUI(self):
    ## 페이지 크기 설정 ##
    self.label_pageSize = QLabel('페이지 크기', self)

    cb_pageSize = QComboBox(self)
    cb_pageSize.addItem('A3')
    cb_pageSize.addItem('A4')
    cb_pageSize.addItem('A5')
    cb_pageSize.addItem('B3')
    cb_pageSize.addItem('B4')
    cb_pageSize.addItem('B5')
    cb_pageSize.addItem('커스텀')
    cb_pageSize.activated[str].connect(self.setPageSize)

    ## 여백 / 재단 설정 ##
    self.label_padding = QLabel('재단 길이 설정', self)
    textEdit_padding = QLineEdit()

    ## PDF 저장 경로 설정 ##
    self.layout_pdfSetting = QHBoxLayout()
    self.pdf_path = QLineEdit()
    btn_pdf_path = QPushButton('PDF 저장 경로 선택')
    self.layout_pdfSetting.addWidget(self.pdf_path)
    self.layout_pdfSetting.addWidget(btn_pdf_path)

    layout_pageOption = QVBoxLayout()
    layout_pageOption.setSpacing(15)
    layout_pageOption.setAlignment(Qt.AlignTop)
    layout_pageOption.setContentsMargins(20, 20, 20, 20)
    layout_pageOption.addWidget(self.label_pageSize)
    layout_pageOption.addWidget(cb_pageSize)
    layout_pageOption.addWidget(self.label_padding)
    layout_pageOption.addWidget(textEdit_padding)

    layout_btn = QHBoxLayout()
    layout_btn.setContentsMargins(20, 0, 20, 20)
    self.btn_cancel = QPushButton('취소')
    self.btn_cancel.clicked.connect(self.reject)
    self.btn_cancel.setAutoDefault(False)
    self.btn_ok = QPushButton('확인')
    self.btn_ok.clicked.connect(self.accept)
    self.btn_ok.setDefault(True)
    self.btn_ok.setAutoDefault(True)
    layout_btn.addWidget(self.btn_cancel, stretch=2)
    layout_btn.addWidget(self.btn_ok, stretch=2)

    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.addLayout(layout_pageOption, stretch=1)
    main_layout.addLayout(self.layout_pdfSetting, stretch=1)
    main_layout.setSpacing(20)
    main_layout.addLayout(layout_btn, stretch=1)

    self.setLayout(main_layout)

    ## 이벤트 핸들러 ##
    btn_pdf_path.clicked.connect(self.showPathDialog)

  def setPageSize(self, text):
    return 0
  
  def showPathDialog(self):
    pdf_folder = QFileDialog.getExistingDirectory(self, 'PDF를 저장할 폴더 선택', "./")
    if pdf_folder:
      self.pdf_path.setText(pdf_folder)
