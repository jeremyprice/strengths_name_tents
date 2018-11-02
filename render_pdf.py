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
import reportlab.platypus
from PIL import Image

PAGE_WIDTH, PAGE_HEIGHT = pagesizes.LETTER
text_start_y = PAGE_HEIGHT / 2.0 - (1.5*inch)
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

def print_image(name, image, canvas):
    canvas.setFont('Comic B', 40)
    canvas.setStrokeColorRGB(0.0, 0.0, 0.0)
    canvas.setFillColorRGB(0.0, 0.0, 0.0)
    y = text_start_y - (1.*large_line_spacing)
    canvas.drawCentredString(PAGE_WIDTH/2.0, y, name)
    im = Image.open(image)
    im_w, im_h = im.size
    new_height = large_line_spacing * 1.5
    scale = new_height / im_h
    new_width = im_w * scale
    y = text_start_y
    x = (PAGE_WIDTH / 2) - (new_width / 2)
    #TODO: center picture and scale appropriately
    reportlab.platypus.Image(image, width=new_width, height=new_height).drawOn(canvas, x, y)

def print_talents(talents, canvas):
    canvas.setFont('Comic B', 25)
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

def create_name_tent(fname, name, talents, title=None, image=None):
    load_fonts()
    if title is None:
        title = 'Top {} Talents'.format(num2words(len(talents)).capitalize())
    canvas = create_pdf_canvas(fname)
    # print the right side up side
    if image:
        print_image(name, image, canvas)
    else:
        print_name(name, canvas)
        print_title(title, canvas)
    print_talents(talents, canvas)
    # print the upside down side
    canvas.saveState()
    canvas.translate(PAGE_WIDTH, PAGE_HEIGHT)
    canvas.rotate(180)

    if image:
        print_image(name, image, canvas)
    else:
        print_name(name, canvas)
        print_title(title, canvas)
    print_talents(talents, canvas)
    canvas.restoreState()
    canvas.showPage()
    canvas.save()

def main():
    if os.path.isfile(sys.argv[1]):
        image = sys.argv[1]
        name = sys.argv[2]
        talents = sys.argv[3:]
        create_name_tent('{}_strengths.pdf'.format(name), name, talents, image=image)
    else:
        if len(sys.argv) < 3:
            print('Usage: {} <name> <strength1> ... <strengthN>'.format(sys.argv[0]))
            raise SystemExit(-1)
        name = sys.argv[1]
        talents = sys.argv[2:]
        create_name_tent('{}_strengths.pdf'.format(name), name, talents)

if __name__ == '__main__':
    main()
