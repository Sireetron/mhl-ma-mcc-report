
# from reportlab.pdfgen import canvas
# from utils.font import add_font
# from sections.first_page import draw_first_page
# from sections.DataBase.database_report import db
from sections.SLC.slc import slc
from sections.NginX.nginx import nginx
from sections.Audittrail.audittrail import auditrail
from sections.IOT.iot import iot
# from sections.Airflow.airflow_report_ma_last import airflow



from docxtpl import DocxTemplate, InlineImage
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.shared import Cm
from docx.shared import Inches
from datetime import datetime, timedelta
from datetime import date
from itertools import chain
import os

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
    print("\033[1;31;40m" + f' Loading Report เดือน  {month} ปี  {year}' + "\033[0m")
    doc = DocxTemplate("./sections/Template/Template Report MA 040167.docx")
    merged_bio =  slc(month, year, day, doc, InlineImage)
    # {'day':day,'month':month,'year':year,**nginx(month, year, doc, InlineImage),**auditrail(month, year, doc, InlineImage),**iot(month, year, doc, InlineImage), **slc(month, year, day, doc, InlineImage)}

    # airflow(month, year, doc, InlineImage)
    # db(month, year, doc, InlineImage)
    # {'month':month,'year':year,**nginx(month, year, doc, InlineImage),**auditrail(month, year, doc, InlineImage),**iot(month, year, doc, InlineImage), **slc(month, year, day, doc, InlineImage),**db(month, year, doc, InlineImage)}
    # os.remove(["./sections/NginX/Image/topcountry.png","./sections/NginX/Image/topcountry.png","./sections/NginX/Image/topcountry.png"])
    # /////////////////////////
    
    # if os.path.exists("./sections/NginX/Image/topcountry.png"):
    #     os.remove("demofile.txt")
    # else:
    #     print("The file does not exist")


    doc.render(merged_bio)

    doc.save(f'./sections/Report/รายงานประจำเดือน{month}_{year}.docx')
    
    print("\033[1;31;40m" + f'Done' + "\033[0m")


if __name__ == "__main__":
    main()