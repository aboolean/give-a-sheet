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
    borderless=0,
    guideline=1,
    guidespace=1.25 * inch,
    guidewidth=1,
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
    borderless -- overrides layout and produces end-to-end page
    guideline -- flag for including the left margin line on borderless page
    guidespace -- space of left margin line from page edge
    guidewidth -- width of left margin line
    """

    page = canvas.Canvas(filename, pagesize=pagesize)

    if borderless:
        squareSection(
            page=page,
            location=(0, 0),
            size=pagesize,
            gridspace=gridspace,
            linefreq=0,
            checkered=checkered,
            rainbow=rainbow,
            gridline=gridline,
            boxline=0,
            checkeredcolor=checkeredcolor,
            gridcolor=gridcolor,
            boxcolor=boxcolor,
            bgndcolor=bgndcolor,
            )
        if guideline:
            page.setStrokeColor(grey(boxcolor))
            page.setLineWidth(guidewidth)
            page.line(guidespace, 0, guidespace, pagesize[1])
    else:

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

        for loc in frame_locs:
            squareSection(
                page=page,
                location=loc,
                size=(area_w, area_h),
                gridspace=gridspace,
                linefreq=0,
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


def squareSection(
    page,
    location,
    size,
    gridspace,
    linefreq,
    checkered,
    rainbow,
    gridline,
    linewidth,
    boxline,
    checkeredcolor,
    gridcolor,
    linecolor,
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
    linefreq -- frequency of lines expressed as the number of rows per line
    checkered -- true for checkered grid
    rainbow -- true for rainbow grid
    gridline -- thickness of lines around cells
    linewidth -- width of each writing line
    boxline -- thickness of border around graph(s), 0 for no box
    checkeredcolor -- color of checkered boxes
    gridcolor -- color of grid lines around cells
    linecolor -- color of each line
    boxcolor -- color of box surrounding graph(s)
    bgndcolor -- color of background of each cell
    """

    # dimensions and spacing

    (area_w, area_h) = size
    (loc_x, loc_y) = location

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

    # writing lines

    if linefreq != 0:
        style = TableStyle()
        for line in xrange(int(cells_y / linefreq) + 1):
            rowline = line * linefreq
            style.add('LINEABOVE', (0, rowline), (-1, rowline), linewidth,
                      grey(linecolor))
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


def dual(
    filename,
    pagesize=letter,
    margins=0.5 * inch,
    spacer=0.25 * inch,
    gridspace=0.25 * inch,
    linefreq=1,
    gridline=0.5,
    linewidth=1,
    boxline=1,
    checkered=0,
    rainbow=0,
    checkeredcolor=10,
    gridcolor=20,
    boxcolor=80,
    linecolor=50,
    bgndcolor=0,
    layout=(1, 1),
    borderless=0,
    guideline=1,
    guidespace=1.25 * inch,
    guidewidth=1,
    **excessParams
    ):
    """
    Generates a page that is squared between lines.

    Keyword arguments:
    filename -- output PDF document name
    pagesize -- size of page as (width, height) tuple
    margins -- size of margins around page
    spacer -- size of spacing between graphs
    gridspace -- size of individual grid cells
    linefreq -- frequency of lines expressed as the number of rows per line
    gridline -- thickness of lines around cells
    linewidth -- width of each writing line
    boxline -- thickness of border around graph(s), 0 for no box
    checkered -- true for checkered grid
    rainbow -- true for rainbow grid coloring
    checkeredcolor -- color of checkered boxes
    gridcolor -- color of grid lines around cells
    boxcolor -- color of box surrounding graph(s)
    linecolor -- color of each line
    bgndcolor -- color of background of each cell
    layout -- number of graphs per page in (x, y) tuple
    borderless -- overrides layout and produces end-to-end page
    guideline -- flag for including the left margin line on borderless page
    guidespace -- space of left margin line from page edge
    guidewidth -- width of left margin line
    """

    page = canvas.Canvas(filename, pagesize=pagesize)

    if borderless:
        above = 1 * inch
        below = 0.3 * inch
        cells_y = (pagesize[1] - above - below) / gridspace
        grid_h = cells_y * gridspace
        loc = (0, pagesize[1] - above - grid_h)
        size = (pagesize[1], grid_h)
        squareSection(
            page=page,
            location=loc,
            size=size,
            gridspace=gridspace,
            linefreq=linefreq,
            checkered=checkered,
            rainbow=rainbow,
            gridline=gridline,
            linewidth=linewidth,
            boxline=0,
            checkeredcolor=checkeredcolor,
            gridcolor=gridcolor,
            linecolor=linecolor,
            boxcolor=boxcolor,
            bgndcolor=bgndcolor,
            )
        if guideline:
            page.setStrokeColor(grey(boxcolor))
            page.setLineWidth(guidewidth)
            page.line(guidespace, 0, guidespace, pagesize[1])
    else:

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

        for loc in frame_locs:
            squareSection(
                page=page,
                location=loc,
                size=(area_w, area_h),
                gridspace=gridspace,
                linefreq=linefreq,
                checkered=checkered,
                rainbow=rainbow,
                gridline=gridline,
                linewidth=linewidth,
                boxline=boxline,
                checkeredcolor=checkeredcolor,
                gridcolor=gridcolor,
                linecolor=linecolor,
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


def dotted(
    filename,
    pagesize=letter,
    margins=0.5 * inch,
    spacer=0.25 * inch,
    gridspace=0.25 * inch,
    dotsize=0.5 * mm,
    boxline=0,
    rainbow=0,
    dotcolor=40,
    boxcolor=80,
    bgndcolor=0,
    layout=(1, 1),
    borderless=0,
    guideline=1,
    guidespace=1.25 * inch,
    guidewidth=1,
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
    borderless -- overrides layout and produces end-to-end page
    guideline -- flag for including the left margin line on borderless page
    guidespace -- space of left margin line from page edge
    guidewidth -- width of left margin line
    """

    page = canvas.Canvas(filename, pagesize=pagesize)

    if borderless:
        dotSection(
            page=page,
            location=(0, 0),
            size=pagesize,
            gridspace=gridspace,
            dotsize=dotsize,
            boxline=0,
            rainbow=rainbow,
            dotcolor=dotcolor,
            boxcolor=boxcolor,
            bgndcolor=bgndcolor,
            )
        if guideline:
            page.setStrokeColor(grey(boxcolor))
            page.setLineWidth(guidewidth)
            page.line(guidespace, 0, guidespace, pagesize[1])
    else:

        # dimensions and layout

        (up_w, up_h) = (layout if layout > (0, 0) else (1, 1))
        (page_w, page_h) = pagesize
        (area_w, area_h) = ((page_w - 2 * margins - (up_w - 1) * spacer)
                            / up_w, (page_h - 2 * margins - (up_h - 1)
                            * spacer) / up_h)

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
        radius=gridspace / 3,
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
                page.circle(x_cen=x, y_cen=y, r=dotsize / 2, stroke=0, fill=1)
            else:
                page.setFillColor(grey(dotcolor))
                page.circle(x_cen=x, y_cen=y, r=dotsize / 2, stroke=0, fill=1)

            y += gridspace
        x += gridspace


if __name__ == '__main__':

    # cartesian(
    #     'output.pdf',
    #     spacer=0.1 * inch,
    #     boxline=2,
    #     gridspace=0.25 * inch,
    #     bgndcolor=3,
    #     gridcolor=0,
    #     gridline=1,
    #     boxcolor=50,
    #     layout=(3, 7),
    #     checkered=0,
    #     rainbow=0,
    #     borderless=1,
    #     marginline=1,
    #     )

    # dotted(
    #     "output.pdf",
    #     pagesize=letter,
    #     margins=0.5 * inch,
    #     spacer=0.25 * inch,
    #     gridspace=0.25 * inch,
    #     dotsize=0.5 * mm,
    #     boxline=1,
    #     rainbow=0,
    #     dotcolor=40,
    #     boxcolor=80,
    #     bgndcolor=0,
    #     layout=(2,2),
    #     borderless=1,
    #     guideline=1,
    #     guidespace=1.25 * inch,
    #     guidewidth=1)

    dual(
        'output.pdf',
        pagesize=letter,
        margins=0.5 * inch,
        spacer=0.25 * inch,
        gridspace=0.25 * inch,
        linefreq=1,
        gridline=0.5,
        linewidth=1,
        boxline=1,
        checkered=0,
        rainbow=0,
        checkeredcolor=10,
        gridcolor=20,
        boxcolor=80,
        linecolor=50,
        bgndcolor=0,
        layout=(1, 1),
        borderless=1,
        guideline=1,
        guidespace=1.25 * inch,
        guidewidth=1,
        )
