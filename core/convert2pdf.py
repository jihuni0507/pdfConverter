from PIL import Image
import os

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import io

def convert2PDF(img_sources=[], padding=[], pdf_path='', pageSize=A4):
  pdf = canvas.Canvas(pdf_path, pagesize=pageSize)
  pageWidth, pageHeight = pageSize

  # img_sources의 element 구조: [path, x1, y1, x2, y2] (비율로 받음)
  # padding 구조: [좌측, 상단, 우측, 하단]
  for img_info in img_sources:
    path_img, x1_rel, y1_rel, x2_rel, y2_rel = img_info
    img = Image.open(path_img)
    img_width, img_height = img.size

    x1 = x1_rel * img_width
    y1 = y1_rel * img_height
    x2 = x2_rel * img_width
    y2 = y2_rel * img_height

    img_cropped = img.crop((x1, y1, x2, y2))
    if padding:
      x += padding[0]
      y += padding[3]
      w = pageWidth - padding[0] - padding[2]
      h = pageHeight - padding[1] - padding[3]
    else:
      x = 0
      y = 0
      w = pageWidth
      h = pageHeight

    img_resized = img_cropped.resize((int(w),int(h)))

    img_byte_arr = io.BytesIO()
    img_resized.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    img_reader = ImageReader(img_byte_arr)

    pdf.drawImage(img_reader, x, y, width=w, height=h)
    pdf.showPage()

  pdf.save()