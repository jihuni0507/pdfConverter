from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QWheelEvent
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

    self.btn_close = QPushButton('닫기')
    self.btn_close.clicked.connect(self.accept)

    layout = QVBoxLayout()
    layout.addWidget(self.viewer)
    layout.addWidget(self.btn_close)
    self.setLayout(layout)

  def wheelEvent(self, event: QWheelEvent):
    zoom_in = 1.25
    zoom_out = 1 / 1.25
    if event.angleDelta().y() > 0:
      zoom_factor = zoom_in
    else:
      zoom_factor = zoom_out
    self.viewer.scale(zoom_factor, zoom_factor)