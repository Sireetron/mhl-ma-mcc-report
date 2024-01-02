
# from reportlab.pdfgen import canvas
# from utils.font import add_font
from sections.first_page import draw_first_page
from sections.SLC.slc import slc
from sections.NginX.nginx import nginx
from sections.Audittrail.audittrail import auditrail
from sections.IOT.iot import iot
from sections.DataBase.database_report import db



from docxtpl import DocxTemplate, InlineImage
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.shared import Cm
from docx.shared import Inches
from datetime import datetime, timedelta
from datetime import date
from itertools import chain

# Returns the current local date
first_day_of_current_month = datetime.now().replace(day=1)
last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
# ////
# month = last_day_of_previous_month.month
month = 12
year = 2023
# year = datetime.now().year
day = datetime.now().day

print('last_day_of_previous_month',last_day_of_previous_month.month)
print('month',month)
print('year',year)
print('day',day)

def main():
    # add_font()
    doc = DocxTemplate("./sections/Template/Template copy 2.docx")
    # my_path='/Users/mh-air/Desktop/fhon/python/mhl-ma-report/sections/Templateall.docx'
    # c = canvas.Canvas(my_path,bottomup=0)
    # draw_first_page(c)
    merged_bio =  {**db(month, year, doc, InlineImage), **nginx(month, year, doc, InlineImage), **slc(month, year, day, doc, InlineImage),**auditrail(month, year, doc, InlineImage),**iot(month, year, doc, InlineImage)}
    # print('merge', merged_bio)
    # c.showPage() # saves current page
    # c.save()
    doc.render(merged_bio)
    doc.save(f'./sections/Report/รายงานประจำเดือน{month}_{year}.docx')
    # doc.save('./sections/Report/db.docx')


if __name__ == "__main__":
    main()
