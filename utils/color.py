
from reportlab.lib.pagesizes import A4

main_blue = '#4FACE6'


def set_background_color(c,color=main_blue):
    c.setFillColor(color)
    c.rect(0,0,A4[0],A4[1],fill=1)