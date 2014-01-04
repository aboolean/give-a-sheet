import math
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Frame
from reportlab.pdfbase.pdfform import textFieldAbsolute

from Logo import placeLogo

# ASCII Model

# - : key and legend
# ? : topics
# @ : weekdays
# # : writable area

# #####################################|####################################
# ####------------#####################|######################-------------#
# ####------------#####################|######################-------------#
# #####################################|####################################
# #####################################|####################################
# ####                               ##|#####                              #
# #### @@@@@@@@@ @@@@@@@@@ @@@@@@@@@ ##|##### @@@@@@@@@ @@@@@@@@@ @@@@@@@@ #
# #### @@@@@@@@@ @@@@@@@@@ @@@@@@@@@ ##|##### @@@@@@@@@ @@@@@@@@@ @@@@@@@@ #
# #                                  ##|##                                 #
# # ?? ######### ######### ######### ##|## ?? ######### ######### ######## #
# # ?? ######### ######### ######### ##|## ?? ######### ######### ######## #
# # ?? ######### ######### ######### ##|## ?? ######### ######### ######## #
# #                                  ##|##                                 #
# # ?? ######### ######### ######### ##|## ?? ######### ######### ######## #
# # ?? ######### ######### ######### ##|## ?? ######### ######### ######## #
# # ?? ######### ######### ######### ##|## ?? ######### ######### ######## #
# #                                  ##|##                                 #
# # ?? ######### ######### ######### ##|## ?? ######### ######### ######## #
# # ?? ######### ######### ######### ##|## ?? ######### ######### ######## #
# # ?? ######### ######### ######### ##|## ?? ######### ######### ######## #
# #                                  ##|##                                 #
# # ?? ######### ######### ######### ##|## ?? ######### ######### ######## #
# # ?? ######### ######### ######### ##|## ?? ######### ######### ######## #
# # ?? ######### ######### ######### ##|## ?? ######### ######### ######## #
# #                                  ##|##                                 #
# # ?? ######### ######### ######### ##|## ?? ######### ######### ######## #
# # ?? ######### ######### ######### ##|## ?? ######### ######### ######## #
# #                                  ##|##                                 #
# #####################################|####################################
# #####################################|####################################

def weeklyTodo(
        filename, items, pagesize=letter, margins=0.5*inch, booklet=0,
        binding=0.25*inch, gridline=0.7, gridcolor=20, **excessParams):
    """
    Generates a biweekly todo list booklet.

    Keyword arguments:
    filename -- output PDF document name
    items -- list of topics for a given week
    pagesize -- size of page as (width, height) tuple
    margins -- size of margins around page
    booklet -- flag to generate half-page booklet; full-page if false
    binding -- size of spacing between list and binding on each page
    gridline -- thickness of lines around cells
    gridcolor -- color of grid lines around cells
    """
    # landscape orientation
    if not booklet:
        pagesize = pagesize[::-1]

    # canvas attributes
    page = canvas.Canvas(filename, pagesize=pagesize)
    page.setTitle("Weekly Todo List by Give Sheet")
    page.setAuthor("Andre Aboulian via Give Sheet")
    page.setSubject("Page Template")
    page.setKeywords(['weekly','biweekly','todo','itemized','planner','schedule',
                      'givesheet','pdf','grid','template','paper'])

    _registerFonts([("LearningCurve", "support/fonts/learning_curve/LearningCurve.ttf"),
                   ("OstrichSans", "support/fonts/ostrich/OstrichSans-Medium.ttf"),
                   ("OstrichSans-Bold", "support/fonts/ostrich/OstrichSans-Black.ttf"),
                   ])

    page_w, page_h = pagesize

    # generate pages
    if booklet:
        _makeItemizedTodo(page=page, items=items, origin=(0,0), targetsize=(page_w,page_h/2),
                          margins=margins, binding=binding, gridline=gridline, gridcolor=gridcolor)
        _makeItemizedTodo(page=page, items=items, origin=(0,page_h/2), targetsize=(page_w,page_h/2),
                          margins=margins, binding=binding, gridline=gridline, gridcolor=gridcolor)
        placeLogo(margins, pagesize, canvas, quadrant=1)
        placeLogo(margins, pagesize, canvas, quadrant=4)
    else:
        _makeItemizedTodo(page=page, items=items, origin=(0,0), targetsize=(page_w,page_h),
                          margins=margins, binding=binding, gridline=gridline, gridcolor=gridcolor)
        placeLogo(margins, (page_h, ), canvas, quadrant=4)

    page.save()

def _makeItemizedTodo(page, items, origin, targetsize, margins, binding,
                     gridline, gridcolor, **excessParams):
    """
    Creates a single week of an itemized todo list.

    Keyword arguments:
    page -- a Canvas instance on which to draw
    items -- list of topics for a given week
    origin -- origin of drawing area as (x, y) tuple
    targetsize -- size of target drawing area as (width, height) tuple
    margins -- size of margins around page
    binding -- size of spacing between list and binding on each page
    gridline -- thickness of lines around cells
    gridcolor -- color of grid lines around cells
    """
    page.saveState()

    page.translate(*origin)

    # dimensions and layout
    key_size = 20
    days_label_size = 12
    topic_label_size = 20

    page_w, page_h = targetsize

    area_w, area_h = (page_w - 2*margins - 2*binding) / 2, \
                     (page_h - 2*margins)
    grid_w, grid_h = area_w - topic_label_size, \
                     area_h - key_size - days_label_size
    cell_w, cell_h = grid_w / 3, grid_h / (len(items) + 1)

    if grid_w < 0 or grid_h < 0:
        raise ValueError("The specified dimensions do no fit on the page.")

    # create plain table
    key_row_week = ['','Week:','','']
    key_row_legend = ['','','[legend]','']
    days_row_left = ['', 'Monday', 'Tuesday', 'Wednesday']
    days_row_right = ['', 'Thursday', 'Friday', 'Weekend']
    tasks_rows = [([item] + ['']*3) for item in (items + ['M'])]

    left_data = [key_row_week] + [days_row_left] + tasks_rows
    left_table = Table(left_data, colWidths=([topic_label_size] + [cell_w]*3),
                       rowHeights=([key_size, days_label_size] + [cell_h]*(len(items)+1)))

    right_data = [key_row_legend] + [days_row_right] + tasks_rows
    right_table = Table(right_data, colWidths=([topic_label_size] + [cell_w]*3),
                        rowHeights=([key_size, days_label_size] + [cell_h]*(len(items)+1)))

    # apply table style
    common_style = TableStyle()
    
    common_style.add('VALIGN', (0,1), (-1,-1), 'MIDDLE')
    common_style.add('ALIGN', (0,1), (-1,-1), 'CENTER')

    common_style.add('FONT', (1,1), (-1,1), 'OstrichSans-Bold', 10) # days
    common_style.add('FONT', (0,2), (0,-1), 'OstrichSans', 10) # topics
    common_style.add('ROTATE', (0,2), (0,-1), 90) # topics

    common_style.add('GRID', (0,2), (0,-1), gridline, colors.CMYKColor(black=0.01 * gridcolor)) # topics
    common_style.add('GRID', (1,1), (-1,1), gridline, colors.CMYKColor(black=0.01 * gridcolor)) # days
    common_style.add('LINEBELOW', (1,-1), (-1,-1), gridline, colors.CMYKColor(black=0.01 * gridcolor)) # bottom
    common_style.add('LINEAFTER', (-1,2), (-1,-1), gridline, colors.CMYKColor(black=0.01 * gridcolor)) # right
    common_style.add('INNERGRID', (1,2), (-1,-1), gridline/2, colors.CMYKColor(black=0.01 * gridcolor/2))

    left_table.setStyle(common_style)
    left_table.setStyle(
            TableStyle([('SPAN', (1,0), (2,0)),
                        ('FONT', (1,0), (1,0), 'LearningCurve', 16),
                        ('LINEABOVE', (1,0), (2,0), gridline, colors.CMYKColor(black=0.01 * gridcolor)),
                        ('LINEAFTER', (2,0), (2,0), gridline, colors.CMYKColor(black=0.01 * gridcolor)),
                        ('LINEBEFORE', (1,0), (1,0), gridline, colors.CMYKColor(black=0.01 * gridcolor)),
                        ('ALIGN', (1,0), (1,0), 'LEFT'),
                        ('VALIGN', (1,0), (1,0), 'MIDDLE'),
                        ]))

    right_table.setStyle(common_style)
    right_table.setStyle(
            TableStyle([('SPAN', (2,0), (3,0)),
                        # ('LINEABOVE', (2,0), (3,0), gridline, colors.CMYKColor(black=0.01 * gridcolor)),
                        # ('LINEAFTER', (3,0), (3,0), gridline, colors.CMYKColor(black=0.01 * gridcolor)),
                        # ('LINEBEFORE', (2,0), (2,0), gridline, colors.CMYKColor(black=0.01 * gridcolor)),
                        ('ALIGN', (2,0), (2,0), 'CENTER'),
                        ('VALIGN', (2,0), (2,0), 'MIDDLE'),
                        ]))

    def _drawTable(table, location):
        loc_x, loc_y = location
        frame = Frame(loc_x, loc_y, area_w, area_h, showBoundary=0,
                      leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
        frame.addFromList([table], page)

    # draw individual graphs
    _drawTable(right_table, (margins + area_w + 2*binding, margins))
    _drawTable(left_table, (margins, margins))

    page.restoreState()

# ID number generation
idnum = 0
def _nextID():
    global idnum
    idnum += 1
    return idnum

def _currentID():
    global idnum
    return idnum

def _resetID():
    global idnum
    idnum = 0

def _registerFonts(fontlist):
    from os import path, getcwd, sep
    from inspect import getfile, currentframe
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    try:
        pdfmetrics.getFont(fontlist[0][0])
        return
    except KeyError:
        pass # font not registered

    for fontname, relpath in fontlist:
        selfPath = path.dirname(path.abspath(getfile(currentframe())))
        ttfFile = selfPath + sep + relpath
        pdfmetrics.registerFont(TTFont(fontname, ttfFile))


if __name__ == '__main__':
    weeklyTodo("output.pdf",items=['A','B','C','D'],booklet=1)
