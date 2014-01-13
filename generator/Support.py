#!/usr/bin/python
# -*- coding: utf-8 -*-


def registerFonts(fontlist):
    """
    Registeres specified fonts for use in PDF.

    fontlist -- list of (fontname, relpath) tuples
        fontname -- name for font registration
        relpath -- path to TTF font relative to this function
    """
    from os import path, sep
    from inspect import getfile, currentframe
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    for (fontname, relpath) in fontlist:

        # check if already registered

        try:
            pdfmetrics.getFont(fontname)
            continue  # font already registered
        except KeyError:
            pass  # font not registered

        selfPath = path.dirname(path.abspath(getfile(currentframe())))
        ttfFile = selfPath + sep + relpath
        pdfmetrics.registerFont(TTFont(fontname, ttfFile))
