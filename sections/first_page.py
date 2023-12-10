from reportlab.lib.pagesizes import A4
from utils.color import set_background_color
from utils.position import header
from reportlab.pdfbase.pdfmetrics import stringWidth
from utils.datetime import buddhist_year,thai_month
from reportlab.platypus import Paragraph
from utils.font import bold




def draw_first_page(c):
    set_background_color(c)
    c.setFillColorRGB(1,1,1)
    c.setFont(bold,20)
    c.drawString(header[0],header[1],"Maholan Co,. Ltd")

    c.setFont(bold,44)
    c.drawString(50,200,'รายงานผลการบำรุงรักษา')
    c.drawString(50,260,'และการสำรองข้อมูล')
    c.setFont('Sarabun-Medium',34)
    c.drawString(50,320,f'ประจำเดือน{thai_month} {buddhist_year}')
    return draw_first_page