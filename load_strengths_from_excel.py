#!/usr/bin/env python3

import openpyxl
import sys
import render_pdf

def unwrap_strengths(unw):
    lines = unw.split('\n')
    return [u.split('.')[1].strip() for u in lines]

def BOA_and_McCollum(ws, output_dir):
    for row in ws.iter_rows(min_row=3):
        mentor_name = row[0].value
        mentor_strengths = unwrap_strengths(row[1].value)
        mentee_name = row[3].value
        mentee_strengths = unwrap_strengths(row[4].value)
        fname = '{}/{}.pdf'.format(output_dir, mentor_name)
        render_pdf.create_name_tent(fname, mentor_name, mentor_strengths)
        fname = '{}/{}.pdf'.format(output_dir, mentee_name)
        render_pdf.create_name_tent(fname, mentee_name, mentee_strengths)

def McCollum_HEB_Student_Strengths(ws, output_dir):
    for row in ws.iter_rows(min_row=2):
        mentee_name = row[0].value
        if mentee_name is None:
            continue
        mentee_strengths = [row[1].value, row[2].value, row[3].value]
        fname = '{}/{}.pdf'.format(output_dir, mentee_name)
        render_pdf.create_name_tent(fname, mentee_name, mentee_strengths)

def InspireU_Mentor_Strengths_HEB_McCollum(ws, output_dir):
    for row in ws.iter_rows(min_row=2):
        name = row[0].value
        if name is None:
            continue
        strengths = [row[n].value for n in range(1,6)]
        if None in strengths:
            continue
        fname = '{}/{}.pdf'.format(output_dir, name)
        render_pdf.create_name_tent(fname, name, strengths)

def HEB_Remaining(ws, output_dir):
    for row in ws.iter_rows():
        name = row[0].value
        if name is None:
            continue
        if row[4].value is None:
            upper = 4
        else:
            upper = 6
        strengths = [row[n].value for n in range(1,upper)]
        if None in strengths:
            continue
        fname = '{}/{}.pdf'.format(output_dir, name)
        render_pdf.create_name_tent(fname, name, strengths)

def Harlandale_HEB_Student_Strengths_Tracker(ws, output_dir):
    for row in ws.iter_rows():
        name = row[0].value
        if name is None:
            continue
        strengths = [row[n].value for n in range(1,4)]
        if None in strengths:
            continue
        fname = '{}/{}.pdf'.format(output_dir, name)
        render_pdf.create_name_tent(fname, name, strengths)

def InspireU_Mentor_Strengths_HEB_Harlandale_HS(ws, output_dir):
    for row in ws.iter_rows():
        name = row[0].value
        if name is None:
            continue
        strengths = [row[n].value for n in range(1,6)]
        if None in strengths:
            continue
        fname = '{}/{}.pdf'.format(output_dir, name)
        render_pdf.create_name_tent(fname, name, strengths)

def generic(ws, output_dir):
    # try the age-old one line per person without header line
    # name in the first column
    # strengths in the next columns - 3 for some and 5 for others
    for row in ws.iter_rows():
        name = row[0].value
        if name is None:
            continue
        strengths = [row[n].value for n in range(1,ws.max_column) if row[n].value is not None]
        fname = '{}/{}.pdf'.format(output_dir, name)
        render_pdf.create_name_tent(fname, name, strengths)

def main(xl_fname, output_dir, proc=None):
    wb = openpyxl.load_workbook(xl_fname, read_only=True)
    ws = wb.active
    if proc == 'BOA and McCollum':
        BOA_and_McCollum(ws, output_dir)
    elif proc == 'McCollum HEB Student Strengths':
        McCollum_HEB_Student_Strengths(ws, output_dir)
    elif proc == 'InspireU Mentor Strengths- HEB McCollum':
        InspireU_Mentor_Strengths_HEB_McCollum(ws, output_dir)
    elif proc == 'HEB-remaining':
        HEB_Remaining(ws, output_dir)
    elif proc == 'Harlandale HEB Student Strengths Tracker':
        Harlandale_HEB_Student_Strengths_Tracker(ws, output_dir)
    elif proc == 'InspireU Mentor Strengths- HEB Harlandale HS':
        InspireU_Mentor_Strengths_HEB_Harlandale_HS(ws, output_dir)
    elif proc == 'Holmes Acelity Student Strengths Tracker':
        Harlandale_HEB_Student_Strengths_Tracker(ws, output_dir)
    else:
        generic(ws, output_dir)

if __name__ == '__main__':
    proc = sys.argv[1].split('/')[-1].split('.')[0]
    main(sys.argv[1], sys.argv[2], proc)
