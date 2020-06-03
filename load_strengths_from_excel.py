#!/usr/bin/env python3

import sys
import render_pdf
import render_mini_pdf
import pandas as pd
import numpy as np


def get_name_talents(series):
    name = series['Name']
    talents = (series['S1'], series['S2'], series['S3'], series['S4'], series['S5'])
    return (name, talents)


def main(xlfname, output_dir, imgfname=None, mini=False):
    if mini:
        renderer = render_mini_pdf
    else:
        renderer = render_pdf
    # start with "vRO US and Canada June 2020 Master Roster.xlsx" format
    df = pd.read_excel(xlfname, sheet_name="Roster")
    name_tent = renderer.MultiPageNameTent('{:s}/output.pdf'.format(output_dir))
    spares = []
    if len(df) % 2 == 1:
        # odd
        spares.append(get_name_talents(df.iloc[len(df)-1]))
        end = len(df) - 1
    else:
        end = len(df)
    for row_idx in range(0, end, 2):
        top_name, top_talents = get_name_talents(df.iloc[row_idx])
        bottom_name, bottom_talents = get_name_talents(df.iloc[row_idx + 1])
        if np.nan in top_talents:
            print('Skipping {}: no Strengths'.format(top_name))
            if not np.nan in bottom_talents:
                spares.append((bottom_name, bottom_talents))
            else:
                print('Skipping {}: no Strengths'.format(bottom_name))
            continue
        if np.nan in bottom_talents:
            print('Skipping {}: no Strengths'.format(bottom_name))
            spares.append((top_name, top_talents))
            continue
        name_tent.create_page(top_name, top_talents, bottom_name, bottom_talents, imgfname)
    #TODO: go through the spares and print them
    if len(spares) % 2 == 1:
        # odd
        end = len(spares) - 1
        odd = True
    else:
        end = len(spares)
        odd = False
    for row_idx in range(0, end, 2):
        top_name, top_talents = spares[row_idx]
        bottom_name, bottom_talents = spares[row_idx+1]
        name_tent.create_page(top_name, top_talents, bottom_name, bottom_talents, imgfname)
    if odd:
        top_name, top_talents = spares[-1]
        renderer.create_page(top_name, top_talents, None, None, imgfname)
    name_tent.done()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: {} <xlfname> <output_dir> <imgfname>'.format(sys.argv[0]))
        raise SystemExit()
    main(sys.argv[1], sys.argv[2], sys.argv[3], mini=True)
