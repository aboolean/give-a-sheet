#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Table, TableStyle, Frame, Paragraph
from reportlab.pdfbase.pdfform import textFieldAbsolute

from Logo import placeLogo
from Coloring import grey
from Support import registerFonts


# ASCII Model

# - : key and legend
# ? : topics
# @ : weekdays
## : writable area

#######################################|#####################################
######------------#####################|######################-------------##
######------------#####################|######################-------------##
#######################################|#####################################
#######################################|#####################################
######                               ##|#####                              ##
###### @@@@@@@@@ @@@@@@@@@ @@@@@@@@@ ##|##### @@@@@@@@@ @@@@@@@@@ @@@@@@@@ ##
###### @@@@@@@@@ @@@@@@@@@ @@@@@@@@@ ##|##### @@@@@@@@@ @@@@@@@@@ @@@@@@@@ ##
###                                  ##|##                                 ##
### ?? ######### ######### ######### ##|## ?? ######### ######### ######## ##
### ?? ######### ######### ######### ##|## ?? ######### ######### ######## ##
### ?? ######### ######### ######### ##|## ?? ######### ######### ######## ##
###                                  ##|##                                 ##
### ?? ######### ######### ######### ##|## ?? ######### ######### ######## ##
### ?? ######### ######### ######### ##|## ?? ######### ######### ######## ##
### ?? ######### ######### ######### ##|## ?? ######### ######### ######## ##
###                                  ##|##                                 ##
### ?? ######### ######### ######### ##|## ?? ######### ######### ######## ##
### ?? ######### ######### ######### ##|## ?? ######### ######### ######## ##
### ?? ######### ######### ######### ##|## ?? ######### ######### ######## ##
###                                  ##|##                                 ##
### ?? ######### ######### ######### ##|## ?? ######### ######### ######## ##
### ?? ######### ######### ######### ##|## ?? ######### ######### ######## ##
### ?? ######### ######### ######### ##|## ?? ######### ######### ######## ##
###                                  ##|##                                 ##
### ?? ######### ######### ######### ##|## ?? ######### ######### ######## ##
### ?? ######### ######### ######### ##|## ?? ######### ######### ######## ##
###                                  ##|##                                 ##
#######################################|#####################################
#######################################|#####################################

def itemizedTodo(
    filename,
    items=None,
    pagesize=letter,
    margins=0.5 * inch,
    halfpage=0,
    booklet=0,
    binding=0.25 * inch,
    includeweekend=1,
    collapseweekend=0,
    gridline=0.7,
    gridcolor=20,
    **excessParams
    ):
    """
    Generates a biweekly todo list booklet.

    Keyword arguments:
    filename -- output PDF document name
    items -- list of topics for a given week
    pagesize -- size of page as (width, height) tuple
    margins -- size of margins around page
    halfpage -- two half-page duplicates (portrait), else one full-page spread (landscape)
    booklet -- flag to split columns evenly among two pages, along with left labels
    binding -- size of spacing between designated pages; ignored if 'booklet' is false
    includeweekend -- includes column(s) for weekend, else includes weekdays only and a single notes column
    collapseweekend -- Sat and Sun are collapsed into a single 'Weekend' column and notes column is omitted; ignored if 'includeweekend' is false
    gridline -- thickness of lines around cells
    gridcolor -- color of grid lines around cells
    """

    # full spread: landscape orientation

    if not halfpage:
        pagesize = pagesize[::-1]

    (page_w, page_h) = pagesize

    # default to single list

    if items == None or len(items) < 1:
        items = ['']

    # delermine columns

    weekday_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    if includeweekend:
        if collapseweekend:
            day_labels = weekday_labels + ['Weekend']
        else:
            day_labels = weekday_labels + ['Saturday', 'Sunday'] + ['Notes']
    else:
        day_labels = weekday_labels + ['Notes']

    day_labels_left = day_labels[:len(day_labels) / 2]
    day_labels_right = day_labels[len(day_labels) / 2:]

    # canvas attributes

    page = canvas.Canvas(filename, pagesize=pagesize)
    page.setTitle('Weekly Todo List by Give Sheet')
    page.setAuthor('Andre Aboulian via Give Sheet')
    page.setSubject('Page Template')
    page.setKeywords([
        'weekly',
        'itemized',
        'todo',
        'planner',
        'schedule',
        'givesheet',
        'pdf',
        'grid',
        'template',
        'paper',
        ])

    # register fonts

    registerFonts([('LearningCurve',
                  'support/fonts/learning_curve/LearningCurve.ttf'),
                  ('FreeUniversal',
                  'support/fonts/free_universal/FreeUniversal-Regular.ttf'),
                  ('FreeUniversal-Bold',
                  'support/fonts/free_universal/FreeUniversal-Bold.ttf'),
                  ('FreeUniversal-Italic',
                  'support/fonts/free_universal/FreeUniversal-Italic.ttf')])

    # dimensions and layout

    key_h = 24
    key_w = 100
    key_spacer_above = 0  # space between 'Week' and top margin
    key_spacer_below = 2  # space between 'Week' and grid beneath
    global key_spacer_indent  # space between 'Week' and topic column
    key_spacer_indent = 0
    global key_spacer_left  # space between 'Week' and left margin

    # grid placement

    grids = list()

    if halfpage:

        # orgin -- lower left corner
        # area -- space occupied by week layout
        # grid -- space occupied by individual grids

        (area_w, area_h) = (page_w - 2 * margins, (page_h - 4 * margins) / 2)
        grid_h = area_h - key_h - key_spacer_above - key_spacer_below

        if booklet:

            # half page booklet

            grid_w = (area_w - 2 * binding) / 2
            origin_bottom_left = (margins, margins)
            origin_bottom_right = (page_w / 2 + binding, margins)
            origin_top_left = (margins, page_h / 2 + margins)
            origin_top_right = (page_w / 2 + binding, page_h / 2 + margins)
            grid_size = (grid_w, grid_h)

            grids.append((origin_bottom_left, grid_size, day_labels_left))
            grids.append((origin_bottom_right, grid_size, day_labels_right))
            grids.append((origin_top_left, grid_size, day_labels_left))
            grids.append((origin_top_right, grid_size, day_labels_right))
        else:

        # half page spread

            origin_bottom = (margins, margins)
            origin_top = (margins, page_h / 2 + margins)

            grids.append((origin_top, (area_w, grid_h), day_labels))
            grids.append((origin_bottom, (area_w, grid_h), day_labels))

        placeLogo(margins, pagesize, page, quadrant=1)
        placeLogo(margins, pagesize, page, quadrant=4)
    else:

        (area_w, area_h) = (page_w - 2 * margins, page_h - 2 * margins)
        grid_h = area_h - key_h - key_spacer_above - key_spacer_below

        if booklet:

            # full page booklet

            grid_w = (area_w - 2 * binding) / 2
            origin_left = (margins, margins)
            origin_right = (page_w / 2 + binding, margins)

            grids.append((origin_left, (grid_w, grid_h), day_labels_left))
            grids.append((origin_right, (grid_w, grid_h), day_labels_right))
        else:

        # full page spread

            grids.append(((margins, margins), (area_w, grid_h), day_labels))

        placeLogo(margins, pagesize, page, quadrant=4)

    # draw grids

    for (origin, size, days) in grids:
        _makeGrid(
            page=page,
            items=items,
            days=days,
            origin=origin,
            size=size,
            gridline=gridline,
            gridcolor=gridcolor,
            )

    # draw 'Week' boxes

    def _makeWeekBox(origin):

        # size (key_h, 4*key_w)

        page.circle(origin[0], origin[1], 2)

    key_offset = margins + key_spacer_above + key_h
    if halfpage:
        _makeWeekBox((margins + key_spacer_left, page_h - key_offset))  # top
        _makeWeekBox((margins + key_spacer_left, page_h / 2 - key_offset))  # bottom
    else:
        _makeWeekBox((margins + key_spacer_left, page_h - key_offset))

    # finalize document

    page.save()


def _makeGrid(
    page,
    items,
    days,
    origin,
    size,
    gridline,
    gridcolor,
    **excessParams
    ):
    """
    Creates a single week of an itemized todo list.

    Keyword arguments:
    page -- a Canvas instance on which to draw
    items -- list of topics for a given week
    days -- list of day labels; 'Notes' creates a formatted note column
    origin -- origin of drawing area as (x, y) tuple
    size -- size of grid as (width, height) tuple
    gridline -- thickness of lines around cells
    gridcolor -- color of grid lines around cells
    """

    page.saveState()

    # fonts

    font_topics = 'FreeUniversal-Italic'
    font_days = 'FreeUniversal-Bold'

    # dimensions and layout

    days_label_size = 12
    topic_padding = 2

    (area_w, area_h) = size
    inner_h = area_h - days_label_size
    cell_h = inner_h / len(items)

        # check topic length

    max_topic_len = 40
    for item in items:
        if len(item) > max_topic_len:
            raise ValueError("The topic \'" + item + "\' is " + str(len(item))
                             + ' characters but should be under '
                             + str(max_topic_len) + ' characters.')

        # topic style

    topic_style = ParagraphStyle('TopicStyle')
    topic_style.fontSize = 10
    topic_style.leading = 12
    topic_style.alignment = TA_CENTER
    topic_style.fontName = font_topics
    topic_style.splitLongWords = 1

    topics = list()  # (topic, wrap_length)
    for item in items:
        p = Paragraph(item, topic_style)
        l = p.wrap(cell_h - 2 * topic_padding, 0)[1]
        topics.append((p, l))

        # max label size

    topic_label_size = topic_style.leading
    for (topic, wrap_length) in topics:
        if wrap_length > topic_label_size:
            topic_label_size = wrap_length

    topic_label_size_padded = topic_label_size + 2 * topic_padding  # add padding

    global key_spacer_left, key_spacer_indent
    key_spacer_left = topic_label_size_padded + key_spacer_indent

    inner_w = area_w - topic_label_size_padded
    cell_w = inner_w / len(days)

    if inner_w < 0 or inner_h < 0:
        raise ValueError('Specified dimensions do not fit on page.')

    # create plain table

    days_row = [[''] + days]
    tasks_rows = [[''] * (1 + len(days))] * len(items)

    data = days_row + tasks_rows
    col_w = [topic_label_size_padded] + [cell_w] * len(days)
    row_h = [days_label_size] + [cell_h] * len(items)
    table = Table(data, colWidths=col_w, rowHeights=row_h)

    # apply table style

    table_style = TableStyle()

    table_style.add('VALIGN', (1, 0), (-1, 0), 'MIDDLE')
    table_style.add('ALIGN', (1, 0), (-1, 0), 'CENTER')

    table_style.add('FONT', (1, 0), (-1, 0), font_days, 10)  # days

    table_style.add('GRID', (0, 1), (0, -1), gridline, grey(gridcolor))  # topics
    table_style.add('GRID', (1, 0), (-1, 0), gridline, grey(gridcolor))  # days
    table_style.add('LINEBELOW', (1, -1), (-1, -1), gridline, grey(gridcolor))  # bottom
    table_style.add('LINEAFTER', (-1, 1), (-1, -1), gridline, grey(gridcolor))  # right
    table_style.add('INNERGRID', (1, 1), (-1, -1), gridline / 2,
                    grey(gridcolor))

    table.setStyle(table_style)

    # draw table

    (x_o, y_o) = origin
    frame = Frame(
        x_o,
        y_o,
        area_w,
        area_h,
        leftPadding=0,
        bottomPadding=0,
        rightPadding=0,
        topPadding=0,
        )
    frame.addFromList([table], page)

    # draw topics

    page.rotate(90)  # rotated (y, -x)
    for (i, (topic, wrap_length)) in enumerate(topics):
        middle_comp = 0.5 * (topic_label_size - wrap_length)
        (loc_x, loc_y) = (y_o + i * cell_h, -(x_o + topic_label_size_padded
                          - middle_comp))
        frame = Frame(
            loc_x,
            loc_y,
            cell_h,
            wrap_length + 2 * topic_padding,
            showBoundary=0,
            leftPadding=topic_padding,
            rightPadding=topic_padding,
            topPadding=topic_padding,
            bottomPadding=topic_padding,
            )
        frame.addFromList([topic], page)
    page.rotate(-90)

    # restore canvas state

    page.restoreState()


if __name__ == '__main__':
    itemizedTodo(
        'output.pdf',
        items=[
            '6.002',
            '6.004',
            '6.006',
            '6.831',
            '4.341',
            '21W.789',
            'Miscellanea',
            ][::-1],
        halfpage=1,
        booklet=0,
        includeweekend=0,
        collapseweekend=1,
        gridcolor=60,
        gridline=1,
        )
