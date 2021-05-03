from flask import Flask, render_template, request,redirect, url_for, flash
from werkzeug.utils import secure_filename
from functools import partial

import os

import urllib

from PIL import Image
from dehaze import dehaze

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg','png','JPG','JPEG','PNG'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

app = Flask(__name__)

output_fles = ['dark.jpg','rawt.jpg','refinedt.jpg','radiance-rawt.jpg','radiance-refinedt.jpg']

def generate_results(src, generator):
    im = Image.open(src)
    dark, rawt, refinedt, rawrad, rerad = generator(im)
    UPLOAD_FOLDER = "static/results/"
    im.save(os.path.abspath(UPLOAD_FOLDER + src))
    dark.save(os.path.abspath(UPLOAD_FOLDER+src[:-4]+output_fles[0]))
    rawt.save(os.path.abspath(UPLOAD_FOLDER+src[:-4]+output_fles[1]))
    refinedt.save(os.path.abspath(UPLOAD_FOLDER+src[:-4]+output_fles[2]))
    rawrad.save(os.path.abspath(UPLOAD_FOLDER+src[:-4]+output_fles[3]))
    rerad.save(os.path.abspath(UPLOAD_FOLDER+src[:-4]+output_fles[4]))

@app.route('/index.html')
def home():
    return redirect(url_for('hello_world'))

@app.route('/about.html')
def about():
    return render_template("about.html")

@app.route('/contact.html')
def contact():
    return render_template("contact.html")

@app.route('/upload', methods = ['GET','POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('error.html',message = "Unauthorized Access")
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return render_template('error.html', message="No File Selected")
        if not allowed_file(file.filename):
            return render_template('error.html',message = "Invalid Image File")
        file.filename = secure_filename(file.filename)
        file.save(file.filename)
        generate_results(file.filename, partial(dehaze, tmin=0.2, Amax=170,w=7, r=40))
        return render_template("results.html",img = output_fles + [file.filename])

@app.route('/upload_link', methods = ['GET', 'POST'])
def upload_link():
    if request.method == 'GET':
        return render_template('error.html',message = "Unauthorized Access")
    if request.method == 'POST':
        link = request.form['text']
        if not allowed_file(link):
            return render_template('error.html',message = "Invalid Image Link")
        link = link.rsplit('?',1)[0]
        file_name = link.rsplit('/', 1)[1]
        file_name = secure_filename(file_name)
        try:
            urllib.urlretrieve(link,file_name)
        except:
            return render_template('error.html',message = "Unable to Collect Image from Link")
        generate_results(file_name, partial(dehaze, tmin=0.2, Amax=170, w=15, r=40))
        return render_template("results.html", img=output_fles + [file_name])

@app.route('/')
def hello_world():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug = True)
