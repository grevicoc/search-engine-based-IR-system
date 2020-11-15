from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, abort
from wtforms import Form, StringField, validators, RadioField
from pathlib import Path
from pitonan.mainjson import getsorted,tablemaker
from pitonan.maintxt import getsortedtxt,tablemakertxt
from werkzeug.utils import secure_filename
import pandas as pd
import os

# TODO Bikin sistem upload file
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config["TXT_PATH"] = str(Path('data/txt').absolute())
app.config['UPLOAD_FOLDER'] = str(Path('data/txt').absolute())
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

class searchForm(Form):
    query = StringField('Nyari apa om', [validators.Length(min=1)])
    searchtype = RadioField('Sumber data', choices=[('web', 'Web Scraping'), ('file', 'File Local'),('table1', 'Web Scraping Table'),('table2', 'Local File Table')])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    form = searchForm(request.args)
    return render_template('home.html', form=form)

@app.route('/search')
def search():
    form = searchForm(request.args)
    if request.method == 'GET' and form.validate() and form.searchtype.data == 'web':
        return render_template('search.html', form=form, docs=getsorted(form.query.data))
    
    elif request.method == 'GET' and form.validate() and form.searchtype.data == 'file':
        if sorted(Path(app.config['TXT_PATH']).glob('*.txt')):
            result = getsortedtxt(form.query.data)
            for doc in result:
                filename = doc['link']
                doc['link'] = url_for('txt', txt_name=filename)
            return render_template('search.html', form=form, docs=result)
        else:
            return redirect('upload')

    elif request.method == 'GET' and form.validate() and form.searchtype.data == 'table2':
        form = searchForm(request.args)
        df = tablemakertxt(form.query.data)
        return render_template('table.html',form = form,table = df.to_html(escape=False))

    elif request.method == 'GET' and form.validate() and form.searchtype.data == 'table1':
        form = searchForm(request.args)
        df = tablemaker(form.query.data)
        return render_template('table.html',form = form,table = df.to_html(escape = False))

    else:
        return redirect('/')

@app.route('/txt/<txt_name>')
def txt(txt_name):
    try:
        return send_from_directory(app.config["TXT_PATH"], filename=txt_name, as_attachment=False)
    except FileNotFoundError:
        abort(404)

@app.route('/about')
def about():
    
    return render_template('about.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'txt[]' not in request.files:
            flash('No files uploaded')
            return render_template('upload.html')
        
        files = request.files.getlist('txt[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(Path(app.config['UPLOAD_FOLDER']).joinpath(filename))
    return render_template('upload.html')

@app.route('/deltxt')
def deltxt():
    files = Path(app.config['UPLOAD_FOLDER']).glob('*.txt')
    for file in files:
        os.remove(file)
    return redirect('/upload')


if __name__ == "__main__":
    app.secret_key = '12345'
    app.run(debug=True)