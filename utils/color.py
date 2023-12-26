
from reportlab.lib.pagesizes import A4

## ### total server

blue = '#50ace7'

main_blue = '#4FACE6'


## performance

red = '#ff3131'

yellow = '#ff3131'

green = '#7ed957'

### graph zabbix

pink_dot = '#fc66cc'

purple_dot = '#745cac'

green_dot = '#64d4d4'

## donut chart zabbix

dark_green ='#6aa84f'

soft_green ='#b7d7a8'

dark_yellow= '#f7c927'

soft_yellow ='#fdf2cc'

dark_red = '#cc1a01'

soft_red=' #f5cccc'


def set_background_color(c,color=main_blue):
    c.setFillColor(color)
    c.rect(0,0,A4[0],A4[1],fill=1)