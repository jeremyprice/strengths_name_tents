#!/usr/bin/env python3

from flask import Flask, render_template, request, send_from_directory, abort
import render_pdf
import yaml
import os
import logging
import logging.handlers

DEBUG = False
app_log = logging.getLogger('strengths')
app = Flask(__name__)
strengths_data = yaml.load(open('strengths_data.yml', 'r').read())
strengthsfinder = strengths_data['StrengthsFinderThemes']
s_strengthsfinder = set(strengthsfinder)
strengthsexplorer = strengths_data['StrengthsExplorerThemes']
s_strengthsexplorer = set(strengthsexplorer)
render_pdf.load_fonts()


def setup_paths():
    for req_path in 'pdfs/', 'logs/':
        try:
            os.mkdir(req_path)
        except FileExistsError:
            pass


def setup_logging():
    if DEBUG:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    # send messages to a rotated log file - rotated every monday
    flask_handler = logging.handlers.TimedRotatingFileHandler('./logs/flask.log', when='W0')
    flask_handler.setFormatter(formatter)
    flask_handler.setLevel(loglevel)
    app.logger.addHandler(flask_handler)
    app.logger.setLevel(loglevel)
    app_handler = logging.handlers.TimedRotatingFileHandler('./logs/app.log', when='W0')
    app_handler.setFormatter(formatter)
    app_handler.setLevel(loglevel)
    app_log.addHandler(app_handler)
    app_log.setLevel(loglevel)


@app.route('/')
def index():
    # load index.html through the template engine and fire it at the user
    return render_template('index.html', strengthsfinder=strengthsfinder,
                           strengthsexplorer=strengthsexplorer, input_count=10)


def sanity_checks(name, strengths):
    # get rid of the blank strengths
    strengths = list(filter(lambda x: x != '', strengths))
    if request.form['input-strengths']:
        # check the magical hidden field
        hidden = request.form['input-strengths']
        app_log.error('Got a value in the hidden field (input-strengths): {}'.format(hidden))
        abort(400)
    if not name:
        # check to see that they entered a name
        app_log.error('Name field was blank')
        abort(400)
    if '- StrengthsFinder Themes' in strengths:
        # need to select a strength
        app_log.error('Had the "StrengthsFinder Themes" in the submission')
        abort(400)
    if '- StrengthsExplorer Themes' in strengths:
        # need to select a strength
        app_log.error('Had the "StrengthsExplorer Themes" in the submission')
        abort(400)
    s_strengths = set(strengths)
    if not s_strengths.issubset(s_strengthsfinder) and not s_strengths.issubset(s_strengthsexplorer):
        # not a full set of finder or explorer
        app_log.error('not a full set of explorer or finder talents: {}'.format(strengths))
        abort(400)
    if s_strengths.issubset(s_strengthsfinder) and not (len(strengths) == 5 or len(strengths) == 10):
        # expected 5 talents for finder
        app_log.error('Did not supply 5 finder talents: {}'.format(strengths))
        abort(400)
    if s_strengths.issubset(s_strengthsexplorer) and len(strengths) != 3:
        # expected 3 talents for explorer
        app_log.error('Did not supply 3 explorer talents: {}'.format(strengths))
        abort(400)
    if len(s_strengths) != len(strengths):
        # got a duplicate
        app_log.error('A duplicate strength was submitted: {}'.format(strengths))
        abort(400)
    return strengths


@app.route('/generate', methods=['POST'])
def generate():
    # load info from the post data and generate a PDF and return it
    app_log.info('Got a submission')
    name = request.form.get('nameInput')
    title = request.form.get('titleInput')
    if title == '':
        title = None
    strengths = [request.form.get('inputStrength{}'.format(idx)) for idx in range(1, 11)]
    strengths = sanity_checks(name, strengths)
    app_log.info('Name: {}, Strengths: {}, Title: {}'.format(name, strengths, title))
    fname = '{}_name_tent.pdf'.format(name)
    fdir = 'pdfs/'
    render_pdf.create_name_tent(fdir + fname, name, strengths, title)
    return send_from_directory(fdir, fname)


if __name__ == '__main__':
    setup_paths()
    setup_logging()
    app_log.info('Application started')
    app.run(debug=DEBUG)
