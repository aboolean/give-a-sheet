import math
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Frame

from Logo import placeLogo

def cartesian(
        filename, pagesize=letter, margins=0.5*inch, gridspace=0.25*inch, checkered=0,
        gridline=0.5, boxline=0.5, checkeredcolor=10, gridcolor=20, boxcolor=80, bgndcolor=0,
        persheet=1, **excessParams):
    """
    Generates a page of Cartesian graph paper.

    Keyword arguments:
    filename -- output PDF document name
    pagesize -- size of page as (width, height) tuple
    margins -- size of margins around page (and between graphs)
    gridspace -- size of individual grid cells
    checkered -- true for checkered grid
    gridline -- thickness of lines around cells
    boxline -- thickness of border around graph(s) (keep small)
    checkeredcolor -- color of checkered boxes
    gridcolor -- color of grid lines around cells
    boxcolor -- color of box surrounding graph(s)
    bgndcolor -- color of background of each cell
    persheet -- number of graphs per page, 1-4
    """
    # dimensions
    page_w, page_h = pagesize
    area_w, area_h = page_w - 2*margins, page_h - 2*margins

    # compute grid spacing
    cells_x = int(area_w / gridspace)
    cells_y = int(area_h / gridspace)
    if cells_x < 1 or cells_y < 1:
        raise ValueError("The specified dimensions do no fit on the page.")
    grid_w = (cells_x * (gridspace)) + boxline
    grid_h = (cells_y * (gridspace)) + boxline
    xMargins = (page_w - grid_w) / 2
    yMargins = (page_h - grid_h) / 2

    # create plain table
    data = [['' for col in xrange(cells_x)] for row in xrange(cells_y)]
    table = Table(data, colWidths=gridspace, rowHeights=gridspace)
    
    # checkered grid
    pattern = list()
    if checkered:
        for y in xrange(cells_y):
            for x in xrange(y % 2, cells_x, 2):
                pattern.append(('BACKGROUND',(x,y),(x,y),colors.CMYKColor(black=0.01*checkeredcolor)))
    elif bgndcolor != 0:
        pattern.append(('BACKGROUND',(0,0),(-1,-1),colors.CMYKColor(black=0.01*bgndcolor)))

    # apply table style
    style = TableStyle(pattern)
    style.add('GRID', (0,0), (-1,-1), gridline, colors.CMYKColor(black=0.01*gridcolor))
    style.add('BOX', (0,0), (-1,-1), boxline, colors.CMYKColor(black=0.01*boxcolor))
    table.setStyle(style)

    # draw result
    c  = canvas.Canvas(filename,pagesize=pagesize)
    f = Frame(xMargins, yMargins, grid_w, grid_h, showBoundary=0,
        leftPadding=0, bottomPadding=0,
        rightPadding=0, topPadding=0)
    f.addFromList([table],c)
    placeLogo(margins,pagesize,c)
    c.save()

def polar(
        filename, pagesize=letter, margins=0.5*inch,
        gridline=0.5, boxline=0.5, gridcolor=20, boxcolor=80, bgndcolor=0,
        persheet=1, **excessParams):
    """
    Generates a page of polar graph paper.

    Keyword arguments:
    filename -- output PDF document name
    pagesize -- size of page as (width, height) tuple
    margins -- size of margins around page (and between graphs)
    gridline -- thickness of lines around cells
    boxline -- thickness of border around graph(s) (keep small)
    gridcolor -- color of grid lines around cells
    boxcolor -- color of box surrounding graph(s)
    bgndcolor -- color of background of each cell
    persheet -- number of graphs per page, 1-4
    """
    pass


if __name__ == '__main__':
    cartesian("output.pdf",bgndcolor=5,gridcolor=0,gridline=1,boxcolor=50)
