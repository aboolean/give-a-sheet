import math
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Frame

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
        filename, weekone, weektwo=None, pagesize=letter, margins=0.5*inch,
        binding=0.25*inch, gridline=0.7, gridcolor=20, **excessParams):
    """
    Generates a biweekly todo list booklet.

    Keyword arguments:
    filename -- output PDF document name
    weekone -- list of topics for a given week
    weektwo -- list of topics for an alternate week, None for single week
    pagesize -- size of page as (width, height) tuple
    margins -- size of margins around page
    binding -- size of spacing between list and binding on each page
    gridline -- thickness of lines around cells
    gridcolor -- color of grid lines around cells
    """
    # canvas attributes
    page = canvas.Canvas(filename, pagesize=pagesize)
    page.setTitle("Weekly Todo List by Give Sheet")
    page.setAuthor("Andre Aboulian via Give Sheet")
    page.setSubject("Page Template")
    page.setKeywords(['weekly','biweekly','todo','itemized','planner','schedule',
                      'givesheet','pdf','grid','template','paper'])

    # generate pages
    makeItemizedTodo(page=page, items=weekone, pagesize=pagesize, margins=margins,
                     binding=binding, gridline=gridline, gridcolor=gridcolor, coverpage=1)
    page.showPage() # new page
    if weektwo != None:
        makeItemizedTodo(page=page, items=weektwo, pagesize=pagesize, margins=margins,
                         binding=binding, gridline=gridline, gridcolor=gridcolor)

    placeLogo(margins, pagesize, canvas, quadrant=1)
    placeLogo(margins, pagesize, canvas, quadrant=4)
    
    page.save()

def makeItemizedTodo(page, items, pagesize, margins, binding,
                     gridline, gridcolor, coverpage=0, **excessParams):
    """
    Creates a single week of an itemized todo list.

    Keyword arguments:
    page -- a Canvas instance on which to draw
    items -- list of topics for a given week
    pagesize -- size of page as (width, height) tuple
    margins -- size of margins around page
    binding -- size of spacing between list and binding on each page
    gridline -- thickness of lines around cells
    gridcolor -- color of grid lines around cells
    coverpage -- flag for including cover pages of booklet
    """
    # dimensions and layout
    key_size = 24
    label_size = 14

    page_w, page_h = pagesize

    area_w, area_h = (page_w - 2*margins - 2*binding) / 2, \
                     (page_h - 4*margins) / 2
    grid_w, grid_h = area_w - label_size, \
                     area_h - key_size - label_size
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
    left_table = Table(left_data, colWidths=([label_size] + [cell_w]*3),
                       rowHeights=([key_size, label_size] + [cell_h]*(len(items)+1)))

    right_data = [key_row_legend] + [days_row_right] + tasks_rows
    right_table = Table(right_data, colWidths=([label_size] + [cell_w]*3),
                        rowHeights=([key_size, label_size] + [cell_h]*(len(items)+1)))

    # apply table style
    common_style = TableStyle()
    
    common_style.add('VALIGN', (0,1), (-1,-1), 'MIDDLE')
    common_style.add('ALIGN', (0,1), (-1,-1), 'CENTER')

    # custom font
    import os
    import reportlab
    folder = os.path.dirname(reportlab.__file__) + os.sep + 'fonts'
    afmFile = os.path.join(folder, 'DarkGardenMK.afm')
    pfbFile = os.path.join(folder, 'DarkGardenMK.pfb')
    from reportlab.pdfbase import pdfmetrics
    justFace = pdfmetrics.EmbeddedType1Face(afmFile, pfbFile)
    faceName = 'DarkGardenMK' # pulled from AFM file
    pdfmetrics.registerTypeFace(justFace)
    justFont = pdfmetrics.Font('DarkGardenMK',
    faceName,
                              'WinAnsiEncoding')
    pdfmetrics.registerFont(justFont)

    common_style.add('FONT', (1,1), (-1,1), 'DarkGardenMK', 10)

    common_style.add('GRID', (0,2), (0,-1), gridline, colors.CMYKColor(black=0.01 * gridcolor)) # topics
    common_style.add('GRID', (1,1), (-1,1), gridline, colors.CMYKColor(black=0.01 * gridcolor)) # days
    common_style.add('LINEBELOW', (1,-1), (-1,-1), gridline, colors.CMYKColor(black=0.01 * gridcolor)) # bottom
    common_style.add('LINEAFTER', (-1,2), (-1,-1), gridline, colors.CMYKColor(black=0.01 * gridcolor)) # right
    common_style.add('INNERGRID', (1,2), (-1,-1), gridline/2, colors.CMYKColor(black=0.01 * gridcolor/2))

    left_table.setStyle(common_style)
    left_table.setStyle(
            TableStyle([('SPAN', (1,0), (2,0)),
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

    # calculate quadrant locations
    quad_locs = list() # indicies 0-3 correspond to quadrants I-IV, resp.
    quad_locs.append((margins + area_w + 2*binding, margins + area_h + 2*margins, right_table)) # Q1
    quad_locs.append((margins, margins + area_h + 2*margins, left_table)) # QII
    quad_locs.append((margins, margins, left_table)) # QIII
    quad_locs.append((margins + area_w + 2*binding, margins, right_table)) # QIV

    # draw individual graphs
    for loc_x, loc_y, table in quad_locs:
        frame = Frame(loc_x, loc_y, area_w, area_h, showBoundary=0,
                      leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
        frame.addFromList([table], page)
    if coverpage:
        page.showPage()
        for loc_x, loc_y, table in [quad_locs[0]] + [quad_locs[2]]:
            frame = Frame(loc_x, loc_y, area_w, area_h, showBoundary=0,
                          leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
            frame.addFromList([table], page)


if __name__ == '__main__':
    weeklyTodo("output.pdf",weekone=['A','B','C','D'],weektwo=['1','2','3'])
