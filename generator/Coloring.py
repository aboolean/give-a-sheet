#!/usr/bin/python
# -*- coding: utf-8 -*-

from reportlab.lib import colors


def grey(percentblack):
    """
    Returns a color instance with the specified level of grey.

    Keyword arguments:
    percentblack -- pecent in range [0,100] of black in color
    """

    if percentblack < 0 or percentblack > 100:
        return ValueError('Out of range grey level.')

    return colors.CMYKColor(black=0.01 * percentblack)
