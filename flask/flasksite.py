from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, abort
from wtforms import Form, StringField, validators, RadioField
from pathlib import Path
import pandas as pd
from pitonan.mainjson import getsorted,tablemaker
from pitonan.maintxt import getsortedtxt,tablemakertxt

# TODO Bikin sistem upload file

app = Flask(__name__)
app.config["TXT_PATH"] = str(Path('data/txt').absolute())

class searchForm(Form):
    query = StringField('Nyari apa om', [validators.Length(min=1)])
    searchtype = RadioField('Sumber data', choices=[('web', 'Web Scraping'), ('file', 'File Local'),('table1', 'Web Scraping Table'),('table2', 'Local File Table')])

# kalo mau ngerun install Flask dulu terus "python flasksite.py" di terminal


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
        result = getsortedtxt(form.query.data)
        for doc in result:
            filename = doc['link']
            doc['link'] = url_for('txt', txt_name=filename)
        return render_template('search.html', form=form, docs=result)
    elif request.method == 'GET' and form.validate() and form.searchtype.data == 'table2':
        form = searchForm(request.args)
        df = tablemakertxt(form.query.data)
        '''html = 
        <html>
            <head><title>HTML Pandas Dataframe with CSS</title></head>
                <link rel="stylesheet" type="text/css" href="../static/df_style.css"/>
            <body>
                {table}
             </body>
        </html>.
        
        pd.set_option('colheader_justify', 'center')
        text_file = open("./templates/table.html", "w")
        text_file.write(html.format(table=df.to_html(classes='mystyle')))
        text_file.close()'''
        return render_template('table.html',form = form,table = df.to_html())
    elif request.method == 'GET' and form.validate() and form.searchtype.data == 'table1':
        form = searchForm(request.args)
        df = tablemaker(form.query.data)
        return render_template('table.html',form = form,table = df.to_html())
    else:
        return redirect('/')

@app.route('/txt/<txt_name>')
def txt(txt_name):
    try:
        return send_from_directory(app.config["TXT_PATH"], filename=txt_name, as_attachment=False)
    except FileNotFoundError:
        abort(404)



if __name__ == "__main__":
    app.secret_key = '12345'
    app.run(debug=True)