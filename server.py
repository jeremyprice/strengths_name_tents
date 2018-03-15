#!/usr/bin/env python3

from flask import Flask, render_template, request, send_from_directory
import render_pdf
import yaml
import os

app = Flask(__name__)
strengths_data = yaml.load(open('strengths_data.yml', 'r').read())
strengthsfinder = strengths_data['StrengthsFinderThemes']
strengthsexplorer  = strengths_data['StrengthsExplorerThemes']
render_pdf.load_fonts()
try:
    os.mkdir('pdfs/')
except FileExistsError:
    pass

@app.route('/')
def index():
    # load index.html through the template engine and fire it at the user
    return render_template('index.html', strengthsfinder=strengthsfinder,
                           strengthsexplorer=strengthsexplorer, input_count=5)

def sanity_checks(name, strengths):
    # get rid of the blank strengths
    strengths = list(filter(lambda x: x != '', strengths))
    if not name:
        # check to see that they entered a name
        return False
    if '- StrengthsFinder Themes' in strengths:
        # need to select a strength
        return False
    if '- StrengthsExplorer Themes' in strengths:
        # need to select a strength
        return False
    #TODO: check to make sure we have 3 for explorer or 5 for finder
    #TODO: check to make sure we didn't select an explorer theme and a finder theme
    #TODO: check to make sure no duplicates
    #TODO: return actual errors, not just False
    return strengths

@app.route('/generate', methods=['POST'])
def generate():
    # load info from the post data and generate a PDF and return it
    # TBD - create a url for each new PDF?
    name = request.form.get('nameInput')
    strengths = [request.form.get('inputStrength{}'.format(idx)) for idx in range(1,6)]
    strengths = sanity_checks(name, strengths)
    if not strengths:
        return
    fname = '{}_name_tent.pdf'.format(name)
    fdir = 'pdfs/'
    render_pdf.create_name_tent(fdir + fname, name, strengths)
    return send_from_directory(fdir, fname)

if __name__ == '__main__':
    app.run()
