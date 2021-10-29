from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors

def tablas(datos,nombre):
   
    data = datos

    NameFile = nombre

    pdf = SimpleDocTemplate(
        NameFile,
        pagesize=letter
    )

    table = Table(data)

    stylenew = TableStyle(
        [
        ('BOX',(0,0),(-1,-1),2,colors.black),

        ('LINEBEFORE',(2,1),(2,-1),2,colors.black),
        ('LINEABOVE',(0,2),(-1,2),2,colors.black),

        ('GRID',(0,1),(-1,-1),2,colors.black),
        ]
    )
    table.setStyle(stylenew)

    elems = []
    elems.append(table)

    pdf.build(elems)