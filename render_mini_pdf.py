#!/usr/bin/env python3

import sys
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
# from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib import pagesizes
from reportlab.lib.units import inch
from num2words import num2words
import reportlab.platypus
from PIL import Image

PAGE_WIDTH, PAGE_HEIGHT = pagesizes.LETTER
text_start_y = -0.5*inch
large_line_spacing = 45
small_line_spacing = 32
name_only_spacing = 15
RACKSPACE_RED_RGB = (0.88, 0.15, 0.18)
RACKSPACE_GREY_RGB = (0.2, 0.2, 0.2)
RACKSPACE_TEXT_RGB = (0.25, 0.25, 0.25)
LEFT_X = 0.5 * inch
LEFT_2ND_COL = 2.5 * inch
IMAGE_MAX_WIDTH = LEFT_2ND_COL - LEFT_X
IMAGE_MAX_HEIGHT = 2 * inch


def load_fonts():
    folder = 'font'
    fs_ttf = os.path.join(folder, 'FiraSans-Book.ttf')
    fsb_ttf = os.path.join(folder, 'FiraSans-Bold.ttf')
    pdfmetrics.registerFont(TTFont("FiraSans", fs_ttf))
    pdfmetrics.registerFont(TTFont("FiraSans Bold", fsb_ttf))


def set_pdf_file_defaults(canvas):
    canvas.setAuthor('Rackspace University')
    canvas.setCreator('Rackspace University')
    canvas.setSubject('Top CliftonStrengths Talents')
    canvas.setTitle('Top Talents Name Tent')
    canvas.setPageSize(pagesizes.LETTER)


def create_pdf_canvas(fname):
    canvas = Canvas(fname)
    set_pdf_file_defaults(canvas)
    return canvas


def print_name(name, canvas):
    canvas.setFont('FiraSans', 34)
    canvas.setStrokeColorRGB(*RACKSPACE_RED_RGB)
    canvas.setFillColorRGB(*RACKSPACE_RED_RGB)
    y = text_start_y - name_only_spacing
    canvas.drawString(LEFT_X, y, name)


def print_lines(canvas):
    # draw the line between the name and the strengths
    canvas.setStrokeColorRGB(*RACKSPACE_RED_RGB)
    canvas.setFillColorRGB(*RACKSPACE_RED_RGB)
    canvas.setLineWidth(2)
    y = text_start_y - large_line_spacing
    canvas.line(LEFT_X, y, PAGE_HEIGHT/2 - LEFT_X, y)


def print_fold_cut_lines(canvas):
    # draw the fold line in the middle horizontally
    canvas.setStrokeColorRGB(*RACKSPACE_GREY_RGB)
    canvas.setFillColorRGB(*RACKSPACE_GREY_RGB)
    canvas.setLineWidth(1)
    y = PAGE_HEIGHT / 2
    canvas.line(0, y, PAGE_WIDTH, y)
    # draw the fold line in the middle vertically
    canvas.setStrokeColorRGB(*RACKSPACE_GREY_RGB)
    canvas.setFillColorRGB(*RACKSPACE_GREY_RGB)
    canvas.setLineWidth(1)
    x = PAGE_WIDTH / 2
    canvas.line(x, 0, x, PAGE_HEIGHT)


def print_image(image, canvas, scaling=1.0, font_scaling=1.0):
    im = Image.open(image)
    im_w, im_h = im.size
    new_height = IMAGE_MAX_HEIGHT
    scale = new_height / im_h
    new_width = im_w * scale
    if new_width > IMAGE_MAX_WIDTH:
        # image is too wide
        new_width = IMAGE_MAX_WIDTH
        scale = new_width / im_w
        new_height = im_h * scale
    y = text_start_y - new_height - (2 * large_line_spacing) + (0.4 * small_line_spacing)
    x = LEFT_X
    # TODO: center picture and scale appropriately
    reportlab.platypus.Image(image, width=new_width, height=new_height).drawOn(canvas, x, y)


def print_talents(talents, canvas, right=False):
    canvas.setFont('FiraSans', 22)
    canvas.setStrokeColorRGB(*RACKSPACE_TEXT_RGB)
    canvas.setFillColorRGB(*RACKSPACE_TEXT_RGB)
    y = text_start_y - (2 * large_line_spacing)
    if right:
        x = LEFT_2ND_COL
    else:
        x = LEFT_X
    for idx, talent in enumerate(talents):
        canvas.drawString(x, y, talent)
        y -= small_line_spacing
        if idx == 4:
            x = LEFT_2ND_COL
            y = text_start_y - (2 * large_line_spacing)


def create_name_tent(fname, name, talents, image=None):
    load_fonts()
    canvas = create_pdf_canvas(fname)
    # print the fold and cut lines
    print_fold_cut_lines(canvas)
    # rotate and print the right side
    canvas.saveState()
    canvas.translate(PAGE_WIDTH/2, PAGE_HEIGHT/2)
    canvas.rotate(90)
    if image:
        print_image(image, canvas)
        print_talents(talents, canvas, right=True)
    else:
        print_talents(talents, canvas, right=False)
    print_name(name, canvas)
    print_lines(canvas)
    canvas.restoreState()
    # canvas.saveState()
    # canvas.translate(0, PAGE_HEIGHT)
    # canvas.rotate(270)
    # if image:
    #     print_image(image, canvas)
    #     print_talents(talents, canvas, right=True)
    # else:
    #     print_talents(talents, canvas, right=False)
    # print_name(name, canvas)
    # print_lines(canvas)
    # canvas.restoreState()
    canvas.showPage()
    canvas.save()


def main():
    # 3 general kinds of name tents: top 5 with an image, top 10, top 5 no image
    # all can have title or no title (can add top XX talents for title)
    # option to add Rackspace logo to lower left
    # data can either come through one at a time (manual) or load from Gallup Excel export
    image = sys.argv[1]
    name = sys.argv[2]
    talents = sys.argv[3:8]
    create_name_tent('{}_strengths.pdf'.format(name), name, talents, image=image)


if __name__ == '__main__':
    main()
else:
    load_fonts()