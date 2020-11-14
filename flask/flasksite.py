from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, abort
from wtforms import Form, StringField, validators
from pathlib import Path

app = Flask(__name__)
app.config["TXT_PATH"] = str(Path('data').absolute())

# kalo mau ngerun install Flask dulu terus "python flasksite.py" di terminal
def testquery(query):
    return [
        {
            "judul": "p",
            "sample": "pepepepe",
        },
        {
            "judul": "po",
            "sample": "popopoppop",
        },
        {
            "judul": query,
            "sample": query + query + query
        }
    ]

class searchForm(Form):
    query = StringField('Nyari apa om', [validators.Length(min=1)])

@app.route('/', methods=['GET'])
def home():
    form = searchForm(request.args)
    if request.method == 'GET' and form.validate():
        return redirect('/search')

    return render_template('home.html', form=form)

@app.route('/search')
def search():
    form = searchForm(request.args)
    if request.method == 'GET' and form.validate():
        return render_template('search.html', form=form, docs=testquery(form.query.data))
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