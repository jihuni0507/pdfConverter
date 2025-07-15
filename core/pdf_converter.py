from PIL import Image
from pprint import pprint
import os

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import io

pdfmetrics.registerFont(TTFont('맑은고딕', 'malgun.ttf'))
pdf = canvas.Canvas("test.pdf", pagesize=A4)
pageWidth, pageHeight = A4

path_source = input("Path of source image folder : ")
path_pdf = input("Path of converted pdf : ")
list_source = os.listdir(path_source)

# 재단선/여백 입력
x1_crop, y1_crop = input("크롭 시작점 좌표 (0.0 ~ 1.0 사이) : ").split()
x2_crop, y2_crop = input("크롭 종결점 좌표 (0.0 ~ 1.0 사이) : ").split()
x1_crop, y1_crop, x2_crop, y2_crop = float(x1_crop), float(y1_crop), float(x2_crop), float(y2_crop)
padding = int(input('여백 입력 (양수, px 단위) : '))
if padding < 0:
  padding = 0

for i in list_source:
  path_img = path_source + '\\' + i
  # 이미지 비율
  img = Image.open(path_img)
  img_width, img_height = img.size
  
  if True: # 나중에 조건 추가해서 페이지별로 여백/배율 적용
    x1 = x1_crop * img_width
    y1 = y1_crop * img_height
    x2 = x2_crop * img_width
    y2 = y2_crop * img_height
  
  img_cropped = img.crop((int(x1), int(y1), int(x2), int(y2)))
  x1_image, y1_image = 0, 0
  x2_image, y2_image = pageWidth, pageHeight
  if padding:
    x1_image =+ padding
    y1_image =+ padding
    x2_image =- padding
    y2_image =- padding

  w, h = int(pageWidth-2*padding), int(pageHeight-2*padding)
  img_final = img_cropped.resize((w, h))

  # PIL의 이미지 객체는 drawImage() 메소드에서 활용 불가
  ##### 메모리에서 이미지 바로 사용
  img_byte_arr = io.BytesIO()
  img_final.save(img_byte_arr, format='PNG')
  img_byte_arr.seek(0)
  ##### ImageReader로 변환
  img_reader = ImageReader(img_byte_arr)

  pdf.drawImage(img_reader, padding, padding, width=(pageWidth-2*padding), height=(pageHeight-2*padding))
  pdf.showPage()

pdf.save()