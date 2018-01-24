#!/usr/bin/env python3

import sys
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib import pagesizes
from reportlab.lib.units import inch
from num2words import num2words

PAGE_WIDTH, PAGE_HEIGHT = pagesizes.LETTER
text_start_y = PAGE_HEIGHT / 2.0 - inch
large_line_spacing = 45
small_line_spacing = 35

def load_fonts():
    folder = 'font'
    comic_ttf = os.path.join(folder, 'comic.ttf')
    comicb_ttf = os.path.join(folder, 'comicbd.ttf')
    pdfmetrics.registerFont(TTFont("Comic", comic_ttf))
    pdfmetrics.registerFont(TTFont("Comic B", comicb_ttf))

def set_pdf_file_defaults(canvas):
    canvas.setAuthor('Rackspace University')
    canvas.setCreator('Rackspace University')
    canvas.setSubject('Top Clifton StrengthsFinder Talents')
    canvas.setTitle('Top Talents Name Tent')
    canvas.setPageSize(pagesizes.LETTER)

def create_pdf_canvas(fname):
    canvas = Canvas(fname)
    set_pdf_file_defaults(canvas)
    return canvas

def print_name(name, canvas):
    canvas.setFont('Comic B', 40)
    canvas.setStrokeColorRGB(0.0, 0.0, 0.0)
    canvas.setFillColorRGB(0.0, 0.0, 0.0)
    y = text_start_y
    canvas.drawCentredString(PAGE_WIDTH/2.0, y, name)

def print_title(title, canvas):
    canvas.setFont('Comic B', 32)
    canvas.setStrokeColorRGB(1.0, 0.0, 0.0)
    canvas.setFillColorRGB(1.0, 0.0, 0.0)
    y = text_start_y - large_line_spacing
    canvas.drawCentredString(PAGE_WIDTH/2.0, y, title)

def print_talents(talents, canvas):
    canvas.setFont('Comic B', 30)
    canvas.setStrokeColorRGB(0.0, 0.0, 0.0)
    canvas.setFillColorRGB(0.0, 0.0, 0.0)
    y = text_start_y - (2 * large_line_spacing)
    if len(talents) > 5:
        x = 2.7 * PAGE_WIDTH / 10.0
    else:
        x = PAGE_WIDTH / 2.0
    for idx, talent in enumerate(talents):
        canvas.drawCentredString(x, y, talent)
        y -= small_line_spacing
        if idx == 4:
            x = 7.3 * PAGE_WIDTH / 10.0
            y = text_start_y - (2 * large_line_spacing)

def create_name_tent(fname, name, talents, title=None):
    if title is None:
        title = 'Top {} Talents'.format(num2words(len(talents)).capitalize())
    canvas = create_pdf_canvas('TestTent.pdf')
    # print the right side up side
    print_name(name, canvas)
    print_title(title, canvas)
    print_talents(talents, canvas)
    # print the upside down side
    canvas.saveState()
    canvas.translate(PAGE_WIDTH, PAGE_HEIGHT)
    canvas.rotate(180)
    print_name(name, canvas)
    print_title(title, canvas)
    print_talents(talents, canvas)
    canvas.restoreState()
    canvas.showPage()
    canvas.save()

def main():
    talents = sys.argv[1:]
    load_fonts()
    create_name_tent('TestFonts.pdf', 'Jeremy Price', talents)

if __name__ == '__main__':
    main()
