
from reportlab.pdfgen import canvas
from utils.font import add_font
from sections.first_page import draw_first_page


def main():
    add_font()
    print('Hello')
    my_path='out/my_pdf.pdf'
    c = canvas.Canvas(my_path,bottomup=0)
    draw_first_page(c)
    c.showPage() # saves current page
    c.save()


if __name__ == "__main__":
    main()