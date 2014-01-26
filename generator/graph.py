#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Frame

from logo import placeLogo
from coloring import grey, rainbowGrid


def cartesian(
    filename,
    pagesize=letter,
    margins=0.5 * inch,
    spacer=0.25 * inch,
    gridspace=0.25 * inch,
    gridline=0.5,
    boxline=1,
    checkered=0,
    rainbow=0,
    checkeredcolor=10,
    gridcolor=20,
    boxcolor=80,
    bgndcolor=0,
    layout=(1, 1),
    **excessParams
    ):
    """
    Generates a page of Cartesian graph paper.

    Keyword arguments:
    filename -- output PDF document name
    pagesize -- size of page as (width, height) tuple
    margins -- size of margins around page
    spacer -- size of spacing between graphs
    gridspace -- size of individual grid cells
    gridline -- thickness of lines around cells
    boxline -- thickness of border around graph(s), 0 for no box
    checkered -- true for checkered grid
    rainbow -- true for rainbow grid coloring
    checkeredcolor -- color of checkered boxes
    gridcolor -- color of grid lines around cells
    boxcolor -- color of box surrounding graph(s)
    bgndcolor -- color of background of each cell
    layout -- number of graphs per page in (x, y) tuple
    """

    # dimensions and layout

    (up_w, up_h) = (layout if layout > (0, 0) else (1, 1))
    (page_w, page_h) = pagesize
    area_w = (page_w - 2 * margins - (up_w - 1) * spacer) / up_w
    area_h = (page_h - 2 * margins - (up_h - 1) * spacer) / up_h

    if area_w < 0 or area_h < 0:
        raise ValueError('Specified dimensions do not fit on page.')

    frame_locs = list()

    x = margins  # begin after left margin
    for frame_x in xrange(up_w):
        y = margins  # begin above lower margin
        for frame_y in xrange(up_h):
            frame_locs.append((x, y))
            y += area_h + spacer
        x += area_w + spacer

    # draw result

    page = canvas.Canvas(filename, pagesize=pagesize)
    for loc in frame_locs:
        gridSection(
            page=page,
            location=loc,
            size=(area_w, area_h),
            gridspace=gridspace,
            checkered=checkered,
            rainbow=rainbow,
            gridline=gridline,
            boxline=boxline,
            checkeredcolor=checkeredcolor,
            gridcolor=gridcolor,
            boxcolor=boxcolor,
            bgndcolor=bgndcolor,
            )

    placeLogo(margins, pagesize, canvas, quadrant=4)

    page.setTitle('Cartesian Graph Paper by Give Sheet')
    page.setAuthor('Andre Aboulian via Give Sheet')
    page.setSubject('Page Template')
    page.setKeywords([
        'graph',
        'cartesian',
        'givesheet',
        'pdf',
        'grid',
        'template',
        'paper',
        ])
    page.save()


def gridSection(
    page,
    location,
    size,
    gridspace,
    checkered,
    rainbow,
    gridline,
    boxline,
    checkeredcolor,
    gridcolor,
    boxcolor,
    bgndcolor,
    **excessParams
    ):
    """
    Places a Cartesian graph in the specified location on the canvas.

    Keyword arguments:
    page -- a Canvas instance on which to draw
    location -- location of the graph as a list of (x, y) tuple
    size -- size of the graph as (width, height) tuple
    gridspace -- size of individual grid cells
    checkered -- true for checkered grid
    rainbow -- true for rainbow grid
    gridline -- thickness of lines around cells
    boxline -- thickness of border around graph(s), 0 for no box
    checkeredcolor -- color of checkered boxes
    gridcolor -- color of grid lines around cells
    boxcolor -- color of box surrounding graph(s)
    bgndcolor -- color of background of each cell
    """

    # dimensions and spacing

    (area_w, area_h) = size
    loc_x, loc_y = location

    (cells_x, cells_y) = (int(area_w / gridspace), int(area_h / gridspace))

    grid_w = cells_x * gridspace + boxline
    grid_h = cells_y * gridspace + boxline

    xMargins = (area_w - grid_w) / 2
    yMargins = (area_h - grid_h) / 2

    if cells_x < 1 or cells_y < 1:
        raise ValueError('Specified dimensions do not fit on page.')

    # create plain table

    data = [['' for col in xrange(cells_x)] for row in xrange(cells_y)]
    table = Table(data, colWidths=gridspace, rowHeights=gridspace)

    # checkered grid or shaded background

    pattern = list()

    if checkered and rainbow:
        raise ValueError('Grid pattern cannot be both rainbow and checekred.')

    if checkered:
        for y in xrange(cells_y):
            for x in xrange(y % 2, cells_x, 2):
                c = (x, y)
                pattern.append(('BACKGROUND', c, c, grey(checkeredcolor)))
    elif rainbow:
        rainbow_pattern = rainbowGrid((cells_x, cells_y), darkness=5)
        for x in xrange(cells_x):
            for y in xrange(cells_y):
                c = (x, y)
                pattern.append(('BACKGROUND', c, c, rainbow_pattern[x][y]))
    elif bgndcolor != 0:
        pattern.append(('BACKGROUND', (0, 0), (-1, -1), grey(bgndcolor)))

    # apply table style

    style = TableStyle(pattern)
    style.add('INNERGRID', (0, 0), (-1, -1), gridline, grey(gridcolor))
    if boxline != 0:
        style.add('BOX', (0, 0), (-1, -1), boxline, grey(boxcolor))
    table.setStyle(style)

    # draw graphs

    frame = Frame(
        loc_x + xMargins,
        loc_y + yMargins,
        grid_w,
        grid_h,
        leftPadding=0,
        bottomPadding=0,
        rightPadding=0,
        topPadding=0,
        )
    frame.addFromList([table], page)


def dotted(
    filename,
    pagesize=letter,
    margins=0.5 * inch,
    spacer=0.25 * inch,
    gridspace=0.25 * inch,
    dotsize=0.5 * mm,
    boxline=0,
    rainbow=0,
    dotcolor=50,
    boxcolor=80,
    bgndcolor=0,
    layout=(1, 1),
    **excessParams
    ):
    """
   Generates a page of vertex-dotted grid paper.

    Keyword arguments:
    filename -- output PDF document name
    pagesize -- size of page as (width, height) tuple
    margins -- size of margins around page
    spacer -- size of spacing between grids (if multiple)
    gridspace -- size of individual grid cells, space between dots
    dotsize -- diameter of each individual dot
    boxline -- thickness of border around graph(s), 0 for no box
    rainbow -- true for rainbow dot coloring
    dotcolor -- color of dot at each cell vertex
    boxcolor -- color of box surrounding graph(s)
    bgndcolor -- color of grid background
    layout -- number of graphs per page in (x, y) tuple
    """

    # dimensions and layout

    (up_w, up_h) = (layout if layout > (0, 0) else (1, 1))
    (page_w, page_h) = pagesize
    (area_w, area_h) = ((page_w - 2 * margins - (up_w - 1) * spacer) / up_w,
                        (page_h - 2 * margins - (up_h - 1) * spacer) / up_h)

    if area_w < 0 or area_h < 0:
        raise ValueError('Specified dimensions do not fit on page.')

    frame_locs = list()

    x = margins  # begin after left margin
    for frame_x in xrange(up_w):
        y = margins  # begin above lower margin
        for frame_y in xrange(up_h):
            frame_locs.append((x, y))
            y += area_h + spacer
        x += area_w + spacer

    # draw result

    page = canvas.Canvas(filename, pagesize=pagesize)
    for loc in frame_locs:
        dotSection(
            page=page,
            location=loc,
            size=(area_w, area_h),
            gridspace=gridspace,
            dotsize=dotsize,
            boxline=boxline,
            rainbow=rainbow,
            dotcolor=dotcolor,
            boxcolor=boxcolor,
            bgndcolor=bgndcolor,
            )
    placeLogo(margins, pagesize, canvas, quadrant=4)

    page.setTitle('Dotted Graph Paper by Give Sheet')
    page.setAuthor('Andre Aboulian via Give Sheet')
    page.setSubject('Page Template')
    page.setKeywords([
        'graph',
        'dotted',
        'dots',
        'givesheet',
        'pdf',
        'grid',
        'template',
        'paper',
        ])
    page.save()


def dotSection(
    page,
    location,
    size,
    gridspace,
    dotsize,
    boxline,
    rainbow,
    dotcolor,
    boxcolor,
    bgndcolor,
    **excessParams
    ):
    """
    Places a Cartesian graph in the specified location on the canvas.

    Keyword arguments:
    page -- a Canvas instance on which to draw
    location -- location of the graph as a list of (x, y) tuple
    size -- size of the graph(s) as (width, height) tuple
    gridspace -- size of individual grid cells, space between dots
    dotsize -- diameter of each individual dot
    boxline -- thickness of border around graph(s), 0 for no box
    rainbow -- true for rainbow dot coloring
    dotcolor -- color of dot at each cell vertex
    boxcolor -- color of box surrounding graph(s)
    bgndcolor -- color of grid background
    """

    # dimensions and spacing

    (area_w, area_h) = size
    (loc_x, loc_y) = location

    (cells_x, cells_y) = (int(area_w / gridspace), int(area_h / gridspace))
    if cells_x < 1 or cells_y < 1:
        raise ValueError('Specified dimensions do not fit on page.')

    grid_w = cells_x * gridspace
    grid_h = cells_y * gridspace

    xMargins = (area_w - grid_w) / 2
    yMargins = (area_h - grid_h) / 2

    outerDots = bgndcolor == 0 and boxline == 0

    # draw surrounding box

    page.setStrokeColor(grey(boxcolor))
    page.setFillColor(grey(bgndcolor))
    page.setLineWidth(boxline)
    page.roundRect(
        x=loc_x + xMargins,
        y=loc_y + yMargins,
        width=grid_w,
        height=grid_h,
        radius=gridspace / 2,
        stroke=boxline > 0,
        fill=bgndcolor != 0,
        )

    # starting position and number of dots

    x = loc_x + xMargins
    if not outerDots:
        x += gridspace
        (dots_x, dots_y) = (cells_x - 1, cells_y - 1)
    else:
        (dots_x, dots_y) = (cells_x + 1, cells_y + 1)

    # draw dots

    rainbow_pattern = rainbowGrid((dots_x, dots_y), darkness=50)
    for vert_x in xrange(dots_x):
        y = loc_y + yMargins
        if not outerDots:
            y += gridspace
        for vert_y in xrange(dots_y):
            if rainbow:
                page.setFillColor(rainbow_pattern[vert_x][vert_y])
                page.setLineWidth(dotsize / 10)
                page.setStrokeColor(grey(30))
                page.circle(x_cen=x, y_cen=y, r=dotsize / 2, stroke=1,
                            fill=1)
            else:
                page.setFillColor(grey(dotcolor))
                page.circle(x_cen=x, y_cen=y, r=dotsize / 2, stroke=0,
                            fill=1)

            y += gridspace
        x += gridspace


if __name__ == '__main__':
    cartesian(
        'output.pdf',
        spacer=0.1 * inch,
        boxline=2,
        gridspace=0.25 * inch,
        bgndcolor=5,
        gridcolor=0,
        gridline=1,
        boxcolor=50,
        layout=(3, 7),
        checkered=0,
        rainbow=1,
        )

    # dotted("output.pdf",layout=(3,4),boxline=0,bgndcolor=3,gridspace=0.25*inch,rainbow=1)
