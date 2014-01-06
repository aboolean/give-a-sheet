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
        filename, items=None, shading=None, legend=None, pagesize=letter, margins=0.5*inch, booklet=0,
        binding=0.25*inch, gridline=0.7, gridcolor=20, **excessParams):
    """
    Generates a biweekly todo list booklet.

    Keyword arguments:
    filename -- output PDF document name
    items -- list of topics for a given week
    shading -- a 2D list of topics (rows) vs. days (cols); values indcate percent grey
    legend -- list of 2-item tupes indicating grey value and label
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

    # default to single list
    if items == None or len(items) < 1:
        items = ['']

    # check shading pattern
    if shading != None and (len(shading) != len(items) or not type(shading[0])==list or len(shading[0]) != 6):
        raise ValueError("Shading pattern misformed.")

    # canvas attributes
    page = canvas.Canvas(filename, pagesize=pagesize)
    page.setTitle("Weekly Todo List by Give Sheet")
    page.setAuthor("Andre Aboulian via Give Sheet")
    page.setSubject("Page Template")
    page.setKeywords(['weekly','itemized','todo','itemized','planner','schedule',
                      'givesheet','pdf','grid','template','paper'])

    _registerFonts([("LearningCurve", "support/fonts/learning_curve/LearningCurve.ttf"),
                   ("FreeUniversal", "support/fonts/free_universal/FreeUniversal-Regular.ttf"),
                   ("FreeUniversal-Bold", "support/fonts/free_universal/FreeUniversal-Bold.ttf"),
                   ("FreeUniversal-Italic", "support/fonts/free_universal/FreeUniversal-Italic.ttf"),
                   ])

    page_w, page_h = pagesize

    # generate pages
    if booklet:
        _makeItemizedTodo(
            page=page, items=items, shading=shading, legend=legend, origin=(0,0),targetsize=(page_w,page_h/2),
            margins=margins, binding=binding, gridline=gridline, gridcolor=gridcolor)
        _makeItemizedTodo(
            page=page, items=items, shading=shading, legend=legend, origin=(0,page_h/2), targetsize=(page_w,page_h/2),
            margins=margins, binding=binding, gridline=gridline, gridcolor=gridcolor)
        placeLogo(margins, pagesize, canvas, quadrant=1)
        placeLogo(margins, pagesize, canvas, quadrant=4)
    else:
        _makeItemizedTodo(
            page=page, items=items, shading=shading, legend=legend, origin=(0,0), targetsize=pagesize,
            margins=margins, binding=binding, gridline=gridline, gridcolor=gridcolor)
        placeLogo(margins, pagesize, canvas, quadrant=4)

    page.save()

def _makeItemizedTodo(page, items, shading, legend, origin, targetsize, margins, binding,
                     gridline, gridcolor, **excessParams):
    """
    Creates a single week of an itemized todo list.

    Keyword arguments:
    page -- a Canvas instance on which to draw
    items -- list of topics for a given week
    shading -- a 2D list of topics (rows) vs. days (cols); values indcate percent grey
    legend -- list of 2-item tupes indicating grey value and label
    origin -- origin of drawing area as (x, y) tuple
    targetsize -- size of target drawing area as (width, height) tuple
    margins -- size of margins around page
    binding -- size of spacing between list and binding on each page
    gridline -- thickness of lines around cells
    gridcolor -- color of grid lines around cells
    """
    page.saveState()
    page.translate(*origin)

    # fonts
    font_days = 'FreeUniversal-Bold'
    font_legend = 'FreeUniversal'
    font_topics = 'FreeUniversal-Italic'

    # dimensions and layout
    key_size = 24
    days_label_size = 12
    topic_padding = 2

    page_w, page_h = targetsize
    area_w, area_h = (page_w - 2*margins - 2*binding) / 2, \
                     (page_h - 2*margins)
    grid_h = area_h - key_size - days_label_size
    cell_h = grid_h / (len(items))

        # check topic length
    max_topic_len = 40
    for item in items:
        if len(item) > max_topic_len:
            raise ValueError("The topic \'" + item + "\' is " + str(len(item)) + 
                " characters but should be under " + str(max_topic_len) + " characters.")

        # topic style
    topic_style = ParagraphStyle('TopicStyle')
    topic_style.fontSize = 10
    topic_style.leading = 12
    topic_style.alignment=TA_CENTER
    topic_style.fontName = font_topics
    topic_style.splitLongWords = 1

    topics = list() # (topic, wrap_length)
    for item in items:
        p = Paragraph(item, topic_style)
        l = p.wrap(cell_h - 2*topic_padding, 0)[1]
        topics.append((p,l))

        # max label size
    topic_label_size = topic_style.leading
    for topic, wrap_length in topics:
        if wrap_length > topic_label_size:
            topic_label_size = wrap_length

    topic_label_size_padded = topic_label_size + 2*topic_padding # add padding
    
    grid_w = area_w - topic_label_size_padded
    cell_w = grid_w / 3

    if grid_w < 0 or grid_h < 0:
        raise ValueError("The specified dimensions do not fit on the page.")

    # create legend
    if legend != None:
        legend_data = [[label for grey, label in legend]]
        legend_table = Table(legend_data, colWidths=(min(2*cell_w/len(legend), cell_w)),
                             rowHeights=(key_size - 10))
        legend_table.setStyle(
            TableStyle([('FONT', (0,0), (-1,0), font_legend, 10),
                        ('ALIGN', (0,0), (-1,0), 'CENTER'),
                        ('VALIGN', (0,0), (-1,0), 'MIDDLE'),
                        ('BOX', (0,0), (-1,0), gridline/2, colors.CMYKColor(black=0.01 * gridcolor)),
                        ]))

        legend_shading = TableStyle()
        for i, (grey, label) in enumerate(legend):
            legend_shading.add('BACKGROUND', (i,0), (i,0), colors.CMYKColor(black=0.01 * grey))
        legend_table.setStyle(legend_shading)

    # create plain table
    key_row_week = ['','Week:','','']
    key_row_legend = ['','',legend_table,''] if legend != None else ['']*4
    days_row_left = ['', 'Monday', 'Tuesday', 'Wednesday']
    days_row_right = ['', 'Thursday', 'Friday', 'Weekend']
    tasks_rows = [['']*4]*len(items)

    left_data = [key_row_week] + [days_row_left] + tasks_rows
    left_table = Table(left_data, colWidths=([topic_label_size_padded] + [cell_w]*3),
                       rowHeights=([key_size, days_label_size] + [cell_h]*len(items)))

    right_data = [key_row_legend] + [days_row_right] + tasks_rows
    right_table = Table(right_data, colWidths=([topic_label_size_padded] + [cell_w]*3),
                        rowHeights=([key_size, days_label_size] + [cell_h]*len(items)))

    # apply table style
    common_style = TableStyle()
    
    common_style.add('VALIGN', (0,1), (-1,-1), 'MIDDLE')
    common_style.add('ALIGN', (0,1), (-1,-1), 'CENTER')

    common_style.add('FONT', (1,1), (-1,1), font_days, 10) # days

    common_style.add('GRID', (0,2), (0,-1), gridline, colors.CMYKColor(black=0.01 * gridcolor)) # topics
    common_style.add('GRID', (1,1), (-1,1), gridline, colors.CMYKColor(black=0.01 * gridcolor)) # days
    common_style.add('LINEBELOW', (1,-1), (-1,-1), gridline, colors.CMYKColor(black=0.01 * gridcolor)) # bottom
    common_style.add('LINEAFTER', (-1,2), (-1,-1), gridline, colors.CMYKColor(black=0.01 * gridcolor)) # right
    common_style.add('INNERGRID', (1,2), (-1,-1), gridline/2, colors.CMYKColor(black=0.01 * gridcolor/2))

        # apply shading
    left_shading, right_shading = TableStyle(), TableStyle()
    if shading != None:
        for row in xrange(len(shading)):
            for col in xrange(6):
                grey = shading[row][col]
                if type(grey) == float or type(grey) == int:
                    x, y = col + 1, row + 2 # headings and labels compensation
                    if col < 3:
                        left_shading.add('BACKGROUND', (x,y), (x,y), colors.CMYKColor(black=0.01 * grey))
                    else:
                        x -= 3 # right table compensation
                        right_shading.add('BACKGROUND', (x,y), (x,y), colors.CMYKColor(black=0.01 * grey))

    left_table.setStyle(common_style)
    left_table.setStyle(left_shading)
    left_table.setStyle(
            TableStyle([('SPAN', (1,0), (2,0)),
                        ('FONT', (1,0), (1,0), 'LearningCurve', 18),
                        ('LINEABOVE', (1,0), (2,0), gridline, colors.CMYKColor(black=0.01 * gridcolor)),
                        ('LINEAFTER', (2,0), (2,0), gridline, colors.CMYKColor(black=0.01 * gridcolor)),
                        ('LINEBEFORE', (1,0), (1,0), gridline, colors.CMYKColor(black=0.01 * gridcolor)),
                        ('ALIGN', (1,0), (1,0), 'LEFT'),
                        ('VALIGN', (1,0), (1,0), 'MIDDLE'),
                        ]))

    right_table.setStyle(common_style)
    right_table.setStyle(right_shading)
    right_table.setStyle(
            TableStyle([('SPAN', (2,0), (3,0)),
                        ('ALIGN', (2,0), (2,0), 'CENTER'),
                        ('VALIGN', (2,0), (2,0), 'MIDDLE'),
                        ]))

    def _drawTable(table, location):
        loc_x, loc_y = location
        frame = Frame(loc_x, loc_y, area_w, area_h, showBoundary=0,
                      leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
        frame.addFromList([table], page)

    def _drawTopics(location):
        x_o, y_o = location
        page.rotate(90) # rotated (y, -x)
        for i, (topic, wrap_length) in enumerate(topics):
            middle_comp = 0.5*(topic_label_size - wrap_length)
            loc_x, loc_y = y_o + i*cell_h, \
                           -(x_o + topic_label_size_padded - middle_comp)
            frame = Frame(loc_x, loc_y, cell_h, wrap_length + 2*topic_padding,
                          leftPadding=topic_padding, rightPadding=topic_padding,
                          topPadding=topic_padding, bottomPadding=topic_padding)
            frame.addFromList([topic], page)
        page.rotate(-90)

    # draw individual graphs
    origin_left = (margins, margins)
    origin_right = (margins + area_w + 2*binding, margins)
    _drawTable(left_table, origin_left)
    _drawTable(right_table, origin_right)
    _drawTopics(origin_left)
    _drawTopics(origin_right)

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
