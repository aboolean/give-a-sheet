#!/usr/bin/python
# -*- coding: utf-8 -*-

from reportlab.lib import colors
import random


def grey(percentblack):
    """
    Returns a color instance with the specified level of grey.

    Keyword arguments:
    percentblack -- pecent in range [0,100] of black in color
    """

    if percentblack < 0 or percentblack > 100:
        return ValueError('Out of range grey level.')

    return colors.CMYKColor(black=0.01 * percentblack)


def rainbowGrid(dimensions, darkness=1, scheme=None):
    """
    Returns a 2D list (x,y order) of Color instances forming a rainbow grid.

    Keyword arguments:
    dimensions -- cells in the grid as an (x,y) tuple
    darkness -- darkness of each color, expressed in range [0,100]
    scheme -- a list of Color instances
    """

    # scheme = [colors.HexColor(0xba2742), colors.HexColor(0xd99b50), colors.HexColor(0xf5f573), colors.HexColor(0x688057), colors.HexColor(0x561f91), colors.HexColor(0x94296f)]
    # scheme = [colors.maroon, colors.orangered, colors.gold, colors.olivedrab, colors.ReportLabBlue, colors.indigo, colors.purple]
    # scheme = [colors.red, colors.orange, colors.yellow, colors.green, colors.blue, colors.indigo]
    # scheme = [colors.toColor('rgb(204,0,0)'), colors.toColor('rgb(255,101,59)'), colors.toColor('rgb(245,182,87)'), colors.toColor('rgb(61,122,91)'), colors.toColor('rgb(37,61,129)'), colors.toColor('rgb(83,49,84)')]

    if scheme == None or len(scheme) < 5:
        scheme = [
            colors.firebrick,
            colors.orangered,
            colors.gold,
            colors.olivedrab,
            colors.ReportLabBlue,
            colors.purple,
            ]
    scheme = map(colors.Whiter, scheme, [0.01 * darkness] * len(scheme))
    (w, h) = dimensions
    grid = list()

    for x in xrange(w):
        col = list()
        for y in xrange(h):
            neighbors = list()
            if x > 0:  # above
                neighbors.append(grid[-1][y])
            if y > 0:  # before
                neighbors.append(col[-1])
            if x > 0 and y > 0:  # left diagonal
                neighbors.append(grid[-1][y - 1])
            if x > 0 and y < h - 1:  # right diagonal
                neighbors.append(grid[-1][y + 1])

            chooselist = scheme[:]
            for color in neighbors:
                try:
                    chooselist.remove(color)
                except ValueError:
                    pass
            col.append(random.choice(chooselist))
        grid.append(col)

    return grid


if __name__ == '__main__':
    (w, h) = (17, 24)
    hues = rainbowGrid((w, h), darkness=30)
    from reportlab.pdfgen import canvas
    page = canvas.Canvas('output.pdf', pagesize=(72 * 8.5, 72 * 11))
    for x in xrange(w):
        for y in xrange(h):
            page.setFillColor(hues[x][y])
            width = min(72 * 8.5 / w, 72 * 11 / h)
            page.rect(
                x * width,
                y * width,
                width,
                width,
                fill=1,
                stroke=0,
                )
    page.save()
