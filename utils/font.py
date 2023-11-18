from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os 

bold = 'Sarabun-Bold'
def add_font():
    files = os.listdir('resource/font')
    print(files)
    for file in files:
        pdfmetrics.registerFont(TTFont(file.split('.')[0], f'resource/font/{file}'))

    # pdfmetrics.registerFont(TTFont('THSarabun', 'resource/font/THSarabun.ttf'))
# pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
# pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
# pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))

def test_font():
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch
    from reportlab.lib.pagesizes import letter
    add_font()
    my_path='out/test_font.pdf'# file path
    c = canvas.Canvas(my_path,pagesize=letter)
    c.translate(inch,inch) # starting point of coordinate to one inch
    c.setFillColorRGB(0,0,1) # fill colour
    l1=c.getAvailableFonts() # list of available fonts
    print(l1)
    j=1 # to adjust Y coordinate against each row 
    for my_font in l1: # loop through all fonts 
        c.setFont(my_font,16) # set font family and size    
        c.drawString(inch,j*inch*0.5,my_font)
        j=j+1
    c.setFont('THSarabun',16) # set font family and size    
    c.drawString(inch,j*inch*0.5,my_font)
    c.showPage() # saves current page
    c.save() 
if __name__ == '__main__':
    test_font()