#!/usr/bin/env python3

from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import render_pdf
import yaml
import os
import logging
import logging.handlers

DEBUG = False
app_log = logging.getLogger('strengths')
app = Flask(__name__)
strengths_data = yaml.safe_load(open('strengths_data.yml', 'r').read())
strengthsfinder = strengths_data['StrengthsFinderThemes']
s_strengthsfinder = set(strengthsfinder)
image_options = strengths_data['images']
render_pdf.load_fonts()


def setup_paths():
    for req_path in ('pdfs/', 'logs/', 'python/'):
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
                           image_options=image_options, input_count=10)


def sanity_checks(name, strengths, image, rax_logo):
    # get rid of the blank strengths
    strengths = list(filter(lambda x: x != '', strengths))
    if request.form['input-strengths']:
        # check the magical hidden field
        hidden = request.form['input-strengths']
        app_log.error('Got a value in the hidden field (input-strengths): {}'.format(hidden))
        return "Error: Invalid request values"
    if not name:
        # check to see that they entered a name
        app_log.error('Name field was blank')
        return "Error: you must specify a name"
    if '- StrengthsFinder Themes' in strengths:
        # need to select a strength
        app_log.error('Had the "StrengthsFinder Themes" in the submission')
        return "Error: you didn't select enough talent theme"
    s_strengths = set(strengths)
    if not s_strengths.issubset(s_strengthsfinder):
        # not a full set of finder
        app_log.error('not a full set finder talents: {}'.format(strengths))
        return "Error: you selected some items that are not StrengthsFinder themes"
    if s_strengths.issubset(s_strengthsfinder) and not (len(strengths) == 5 or len(strengths) == 10):
        # expected 5 talents for finder
        app_log.error('Did not supply 5 finder talents: {}'.format(strengths))
        return "Error: must enter 5 or 10 StrengthsFinder talents"
    if len(s_strengths) != len(strengths):
        # got a duplicate
        app_log.error('A duplicate strength was submitted: {}'.format(strengths))
        return "Error: had a duplicate talent in the list"
    if len(strengths) > 5 and image:
        # can only do top 5 with an image
        # trim the Strengths to top 5 only
        app_log.warning('Image selected with more than top 5')
        strengths = strengths[:5]
    return strengths


@app.route('/generate', methods=['POST', 'GET'])
def generate():
    if request.method == 'GET':  # if we have a GET, send them to the root
        return redirect('/')
    # load info from the post data and generate a PDF and return it
    app_log.info('Got a submission')
    name = request.form.get('nameInput')
    title = request.form.get('titleInput')
    image = request.form.get('imageInput')
    if image == "":
        image = None
    else:
        try:
            image = os.path.join('images', image_options[image])
        except KeyError:
            app_log.warning('Invalid image submitted: {}'.format(image))
            image = None
    rax_logo = request.form.get('useLogoInput')
    if rax_logo == "Yes":
        rax_logo = True
    else:
        rax_logo = False
    if title == '':
        title = None
    strengths = [request.form.get('inputStrength{}'.format(idx)) for idx in range(1, 11)]
    strengths = sanity_checks(name, strengths, image, rax_logo)
    if isinstance(strengths, str):
        return strengths, 400
    app_log.info('Name: {}, Strengths: {}, Title: {}'.format(name, strengths, title))
    fname = '{}_name_tent.pdf'.format(name)
    fdir = 'pdfs/'
    render_pdf.create_name_tent(fdir + fname, name, strengths, title, image=image, logo=rax_logo)
    return send_from_directory(fdir, fname, as_attachment=True)


@app.route('/python/')
def python_dir_list():
    files = sorted(os.listdir('python/'))
    return render_template('files.html', files=files, path='Python')


@app.route('/python/<fname>')
def serve_python(fname):
    return send_from_directory('python/', fname)


if __name__ == '__main__':
    setup_paths()
    setup_logging()
    app_log.info('Application started')
    app.run(debug=DEBUG)
