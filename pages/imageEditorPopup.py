from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap, QWheelEvent, QIntValidator, QPainter, QColor, QPen
from PyQt5.QtCore import Qt

class ImageEditorPopup(QDialog):
  def __init__(self, image_path, parent=None):
    super().__init__(parent)
    self.setWindowTitle("이미지 편집")
    self.setMinimumSize(600, 600)

    self.image_path = image_path
    self.viewer = QGraphicsView()
    self.scene = QGraphicsScene(self)
    self.viewer.setScene(self.scene)
    self.viewer.setDragMode(QGraphicsView.ScrollHandDrag)
    self.viewer.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    self.pixmap_item = QGraphicsPixmapItem(QPixmap(self.image_path))
    self.scene.addItem(self.pixmap_item)
    self.viewer.fitInView(self.pixmap_item, Qt.KeepAspectRatio)

    layout = QVBoxLayout()
    layout.addWidget(self.viewer, stretch=10)

    layout_cropInfo = QHBoxLayout()
    layout_cropInfo.setSpacing(20)
    layout_cropInfo.setContentsMargins(40, 10, 40, 10)

    fields = ['x1', 'y1', 'x2', 'y2']
    self.crop_inputs = {}
    for name in fields:
        text_edit = QLineEdit()
        text_edit.setValidator(QIntValidator(0, 10000))
        text_edit.setFixedWidth
        text_edit.setFixedHeight(40)
        text_edit.setPlaceholderText(name.upper())
        self.crop_inputs[name] = text_edit
        layout_cropInfo.addWidget(text_edit)
    # 사용은 self.crop_inputs['x1'].toPlainText() 이런식으로 사용
      
    layout.addLayout(layout_cropInfo, stretch=1)

    layout_btn = QHBoxLayout()
    self.btn_apply = QPushButton('적용')
    self.btn_apply.clicked.connect(self.applyPreview)
    self.btn_cancel = QPushButton('취소')
    self.btn_cancel.clicked.connect(self.reject)
    self.btn_cancel.setAutoDefault(False)
    self.btn_ok = QPushButton('확인')
    self.btn_ok.clicked.connect(self.accept)
    self.btn_ok.setDefault(True)
    self.btn_ok.setAutoDefault(True)
    layout_btn.addStretch(1)
    layout_btn.addWidget(self.btn_apply)
    layout_btn.addWidget(self.btn_cancel)
    layout_btn.addWidget(self.btn_ok)
    
    layout.addLayout(layout_btn)
    self.setLayout(layout)

  def wheelEvent(self, event: QWheelEvent):
    zoom_in = 1.25
    zoom_out = 1 / 1.25
    if event.angleDelta().y() > 0:
      zoom_factor = zoom_in
    else:
      zoom_factor = zoom_out
    self.viewer.scale(zoom_factor, zoom_factor)

  def applyPreview(self):
    x1 = int(self.crop_inputs['x1'].text())
    y1 = int(self.crop_inputs['y1'].text())
    x2 = int(self.crop_inputs['x2'].text())
    y2 = int(self.crop_inputs['y2'].text())
    pixmap = QPixmap(self.image_path)
    painter = QPainter(pixmap)
    pen = QPen(QColor("red"))
    pen.setWidth(3)
    painter.setPen(pen)

    painter.drawRect(x1, y1, x2, y2)
    painter.end()

    self.pixmap_item = QGraphicsPixmapItem(pixmap)
    self.scene.addItem(self.pixmap_item)
    self.viewer.fitInView(self.pixmap_item, Qt.KeepAspectRatio)

  def accept(self):
    try:
      x1 = int(self.crop_inputs['x1'].text())
      y1 = int(self.crop_inputs['y1'].text())
      x2 = int(self.crop_inputs['x2'].text())
      y2 = int(self.crop_inputs['y2'].text())

      if x2 <= x1 or y2 <= y1:
        raise ValueError('좌표 범위가 잘못되었습니다.')
      img = QPixmap(self.image_path)
      width = x2 - x1
      height = y2 - y1

      if x1 < 0 or y1 < 0 or x2 > img.width() or y2 > img.height():
        raise ValueError('이미지 범위 외의 값입니다.')
      
      self.cropped_pixmap = img.copy(x1, y1, width, height)
      super().accept()

    except ValueError as e:
      QMessageBox.warning(self, '입력 오류', str(e))