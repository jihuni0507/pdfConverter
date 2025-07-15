from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QDialog, QComboBox, QLabel, QTextEdit, QPushButton, QFileDialog
from PyQt5.QtCore import Qt

class PageSettingPopup(QDialog):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setWindowTitle("페이지 설정")
    self.setGeometry(300, 300, 500, 800)
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
    textEdit_padding = QTextEdit()

    ## PDF 저장 경로 설정 ##
    self.layout_pdfSetting = QHBoxLayout(self)
    self.pdf_path = QTextEdit()
    btn_pdf_path = QPushButton('PDF 저장 경로 선택')
    self.layout_pdfSetting.addWidget(self.pdf_path)
    self.layout_pdfSetting.addWidget(btn_pdf_path)

    layout = QVBoxLayout()
    layout.addWidget(self.label_pageSize, stretch=1)
    layout.addWidget(cb_pageSize, stretch=1)
    layout.addWidget(self.label_padding, stretch=1)
    layout.addWidget(textEdit_padding, stretch=1)
    layout.addLayout(self.layout_pdfSetting, stretch=2)
    self.setLayout(layout)

    ## 이벤트 핸들러 ##
    btn_pdf_path.clicked.connect(self.showPathDialog)

  def setPageSize(self, text):
    return 0
  
  def showPathDialog(self):
    folderName = QFileDialog.getOpenFileName(self, 'PDF 경로 지정', './')
    if folderName:
      self.pdf_path.setText(folderName)
