#!/usr/bin/env python3

import openpyxl
import sys
import render_pdf

def unwrap_strengths(unw):
    lines = unw.split('\n')
    return [u.split('.')[1].strip() for u in lines]

def main(xl_fname, output_dir):
    wb = openpyxl.load_workbook(xl_fname, read_only=True)
    ws = wb.active
    for row in ws.iter_rows(min_row=3):
        mentor_name = row[0].value
        mentor_strengths = unwrap_strengths(row[1].value)
        mentee_name = row[3].value
        mentee_strengths = unwrap_strengths(row[4].value)
        fname = '{}/{}.pdf'.format(output_dir, mentor_name)
        render_pdf.create_name_tent(fname, mentor_name, mentor_strengths)
        fname = '{}/{}.pdf'.format(output_dir, mentee_name)
        render_pdf.create_name_tent(fname, mentee_name, mentee_strengths)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
