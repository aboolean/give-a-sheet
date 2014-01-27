#!/usr/bin/python
# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Frame

from logo import placeLogo
from coloring import grey, rainbowRow


def lined(
    filename,
    pagesize=letter,
    margins=0.5 * inch,
    spacer=0.25 * inch,
    linespace=9.0 / 32.0 * inch,
    linewidth=0.5,
    boxline=1,
    rainbow=0,
    linecolor=50,
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
    Generates a page of lined paper.

    filename -- output PDF document name
    pagesize -- size of page as (width, height) tuple
    margins -- size of margins around page
    spacer -- size of spacing between graphs
    linespace -- spacing between the lines
    linewidth -- width of each line
    boxline -- thickness of border around graph(s), 0 for no box
    rainbow -- true for rainbow grid coloring
    linecolor -- color of each line
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
        ruleSection(
            page,
            (0, 0),
            pagesize,
            padding=0,
            spacing=linespace,
            above=1 * inch,
            below=0.25 * inch,
            rainbow=rainbow,
            linecolor=linecolor,
            linewidth=linewidth,
            )
        if guideline:
            page.setStrokeColor(grey(linecolor))
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

            # draw surrounding box

            loc_x, loc_y = loc
            page.setStrokeColor(grey(boxcolor))
            page.setFillColor(grey(bgndcolor))
            page.setLineWidth(boxline)
            page.roundRect(
                x=loc_x,
                y=loc_y,
                width=area_w,
                height=area_h,
                radius=linespace / 3,
                stroke=boxline > 0,
                fill=bgndcolor != 0,
                )

            # draw lines

            ruleSection(
                page,
                loc,
                (area_w, area_h),
                padding=2 * mm,
                spacing=linespace,
                above=None,
                below=None,
                rainbow=rainbow,
                linecolor=linecolor,
                linewidth=linewidth,
                )

    placeLogo(margins, pagesize, canvas, quadrant=4)

    page.setTitle('Lined Paper by Give Sheet')
    page.setAuthor('Andre Aboulian via Give Sheet')
    page.setSubject('Page Template')
    page.setKeywords([
        'ruled',
        'lined',
        'lines',
        'givesheet',
        'pdf',
        'template',
        'paper',
        'page',
        ])
    page.save()


def ruleSection(
    page,
    loc,
    size,
    padding=mm,
    spacing=9.0 / 32.0 * inch,
    above=None,
    below=None,
    rainbow=0,
    linecolor=50,
    linewidth=0.5,
    boundingbox=0,
    ):
    """
    Places a quantity of ruled lines in the specified section.

    Keyword arguments:
    page -- a Canvas instance on which to draw
    loc -- location of the section as an (x,y) tuple
    size -- size of the section as (width, height) tuple
    padding -- separation from boundaries of section on each side
    spacing -- spacing between the lines
    above -- space above the first line, defaults to spacing
    below -- minimum space below the last line, defaults to half spacing
    rainbow -- colors the lines in a rainbow pattern, ignoring linecolor
    linecolor -- color of each line
    linewidth -- width of each line
    boundingbox -- draws a box around the section for debugging
    """

    page.saveState()

    # above and below margins

    if above == None:
        above = spacing
    if below == None:
        below = spacing / 4

    # determine spacing

    (loc_x, loc_y) = loc
    (width, height) = size

    area_w = width - 2 * padding
    area_h = height - 2 * padding

    lines = int((area_h - above - below) / spacing) + 1
    if lines < 2:
        raise ValueError('The specified area does not fit any lines.')

    # draw bounding box

    if boundingbox:
        page.setLineWidth(1)
        page.setStrokeColor(colors.black)
        page.rect(loc_x, loc_y, width, height)

    # draw lines

    page.setLineCap(1)
    page.setLineWidth(linewidth)
    page.setStrokeColor(grey(linecolor))

    if rainbow:
        pattern = rainbowRow(lines, darkness=40)

    y = loc_y + height - padding - above
    (x_left, x_right) = (loc_x + padding, loc_x + width - padding)
    for i in xrange(lines):
        if rainbow:
            page.setStrokeColor(pattern[i])
        page.line(x_left, y, x_right, y)
        y -= spacing

    page.restoreState()


if __name__ == '__main__':

    # from reportlab.lib.pagesizes import letter
    # page = canvas.Canvas('output.pdf', pagesize=letter)
    # m = 0.5 * inch
    # (w, h) = letter
    # ruleSection(
    #     page,
    #     (m, m),
    #     (w - 2 * m, h - 2 * m),
    #     boundingbox=0,
    #     linewidth=0.5,
    #     rainbow=1,
    #     )
    # page.save()

    lined(
        'output.pdf',
        pagesize=letter,
        margins=0.5 * inch,
        spacer=0.25 * inch,
        linespace=9.0 / 32.0 * inch,
        linewidth=0.5,
        boxline=1,
        rainbow=0,
        linecolor=50,
        boxcolor=80,
        bgndcolor=0,
        layout=(1, 2),
        borderless=1,
        guideline=1,
        )
