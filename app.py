
from reportlab.pdfgen import canvas
from utils.font import add_font
from sections.first_page import draw_first_page
from sections.SLC.slc import slc
from sections.Audittrail.audittrail import auditrail
from sections.NginX.nginx import nginx
from sections.IOT.iot import iot

from docxtpl import DocxTemplate, InlineImage
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.shared import Cm
from docx.shared import Inches
from datetime import datetime
from datetime import date
from itertools import chain
# Returns the current local date
month = datetime.now().month - 1
year = datetime.now().year
day = datetime.now().day




def main():
    # add_font()
    doc = DocxTemplate("./sections/Template/Template copy 2.docx")
    # my_path='/Users/mh-air/Desktop/fhon/python/mhl-ma-report/sections/Templateall.docx'
    # c = canvas.Canvas(my_path,bottomup=0)
    # draw_first_page(c)
    merged_bio = iot() | nginx() | auditrail() | slc() | {
        'month': month,
        'year' : year,
        'slc_image1': InlineImage(doc, f"./sections/SLC/Image/success.png", width=Cm(5)), 
        'slc_image2': InlineImage(doc, f"./sections/SLC/Image/inprogress.png", width=Cm(5)), 
        'audittrail_image': InlineImage(doc, f"./sections/Audittrail/Image/image.png", width=Cm(16)),
        'nginx_image1': InlineImage(doc, f"./sections/NginX/Image/criticalip.png", width=Cm(16)),
        'nginx_image2': InlineImage(doc, f"./sections/NginX/Image/topcountry.png", width=Cm(16)),
        'nginx_image3': InlineImage(doc, f"./sections/NginX/Image/avgrate.png", width=Cm(16))
    } 
  
    # print(merged_bio)
    # c.showPage() # saves current page
    # c.save()
    doc.render(merged_bio)
    doc.save(f'./sections/Report/รายงานประจำเดือน{month}_{year}.docx')


if __name__ == "__main__":
    main()
