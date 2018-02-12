import os
import reportlab
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

folder = os.path.dirname(reportlab.__file__) + os.sep + 'fonts'
afmFile = os.path.join(folder, 'DarkGardenMK.afm')
pfbFile = os.path.join(folder, 'DarkGardenMK.pfb')
ttfFile = os.path.join(folder, 'Vera.ttf')
justFace = pdfmetrics.EmbeddedType1Face(afmFile, pfbFile)
faceName = 'DarkGardenMK' # pulled from AFM file
pdfmetrics.registerTypeFace(justFace)
justFont = pdfmetrics.Font('DarkGardenMK', faceName, 'WinAnsiEncoding')
pdfmetrics.registerFont(justFont)
pdfmetrics.registerFont(TTFont("Vera", ttfFile))
canvas = Canvas('TestFonts.pdf')
canvas.setFont('DarkGardenMK', 32)
canvas.drawString(10, 150, 'This should be drawn in')
canvas.drawString(10, 100, 'the font DarkGardenMK')
canvas.setFont('Vera', 32)
canvas.drawString(10, 250, 'This should be drawn in')
canvas.drawString(10, 200, 'the font Vera')
canvas.showPage()
canvas.save()
