from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import Form, StringField, validators
import json
import sys
sys.path.append('../')
from tfidf import *


app = Flask(__name__)

# kalo mau ngerun install Flask dulu terus "python flasksite.py" di terminal
def testquery(query):

    #Membaca dbDokumen.txt untuk mendapatkan isi konten artikel
    with open('../dbDokumen.txt') as fin:
        dbDokumen = json.load(fin)

    #Membaca dbArticle.txt untuk mendapatkan data berupa judul, link, dan kalimat pertama dari masing-masing artikel
    with open('../dbArticle.txt') as fin:
        dbArticle = json.load(fin)

    #memasukkan hasil stemming per dokumen ke dalam list stemmed_content
    stemmed_content = [stem(dokumen) for dokumen in dbDokumen] 

    stemmed_content.append(stem(query))
    #print(stemmed_content)

    kolom_vect = setkata(stemmed_content)
    del stemmed_content[-1]


    contents_wcount = [wordcount(content, kolom_vect) for content in stemmed_content]
    idf_vect = idfvect(contents_wcount)
    #print(contents_wcount)

    vect_query = tf(wordcount(stem(query), kolom_vect))
    #print(idf_vect)
    #print(tf_idf(vect_query, idf_vect))


    #tfidf1 = tf_idf(vect_query, idf_vect)
    #print(sum(tfidf1.values()))
    #print(tfidf1.values())
    #print("cosine sim : ",cosine_sim(tfidf1,tfidf1))

    # TODO nanti tiap dokumen di testcorpus dibuat tf_idf dan diitung cosine sim nya
    # yang dibandingin sama vect_query, baru nilai cosine sim itu dijadiin data di dalem
    # dictionary tiap dokumen, dari data itu di sort

    # Mencari cosine sim


    cos = [0 for i in range(len(dbArticle))]
    ti  = [0 for i in range(len(dbArticle))]
    tiq = tf_idf(vect_query,idf_vect)

    for i in range(len(dbArticle)):
        tfd = tf(contents_wcount[i])
        ti[i] = tf_idf(tfd,idf_vect)
        cos[i] = cosine_sim(tiq,ti[i])
        print(cos[i])
        dbArticle[i].update({"similarity" : cos[i]})

    dbArticle = sorted(dbArticle, key = lambda i: i['similarity'],reverse=True)

    return dbArticle

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



if __name__ == "__main__":
    app.secret_key = '12345'
    app.run(debug=True)