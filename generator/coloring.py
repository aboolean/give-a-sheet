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


def rainbowGrid(dimensions, darkness=100, scheme=None):
    """
    Returns a 2D list (x,y order) of Color instances forming a rainbow grid.

    Keyword arguments:
    dimensions -- cells in the grid as an (x,y) tuple
    darkness -- darkness of each color, expressed in range [0,100]
    scheme -- a list of Color instances
    """

    if scheme == None or len(scheme) < 5:
        scheme = [
            colors.firebrick,
            colors.orangered,
            colors.darkgoldenrod,
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


def rainbowRow(length, darkness=100, scheme=None):
    """
    Returns a list of Color instances forming a linear rainbow.

    Keyword arguments:
    length -- number of elements
    darkness -- darkness of each color, expressed in range [0,100]
    scheme -- a list of Color instances
    """

    if scheme == None or len(scheme) < 2:
        scheme = [
            colors.firebrick,
            colors.orangered,
            colors.darkgoldenrod,
            colors.olivedrab,
            colors.ReportLabBlue,
            colors.purple,
            ]
    scheme = map(colors.Whiter, scheme, [0.01 * darkness] * len(scheme))

    line = list()

    chooselist = scheme[:]
    for i in xrange(length):
        if len(chooselist) == 1:
            line.append(chooselist[0])
            chooselist = scheme[:]
            chooselist.remove(line[-1])
        else:
            color = random.choice(chooselist)
            line.append(color)
            chooselist.remove(color)

    return line


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
