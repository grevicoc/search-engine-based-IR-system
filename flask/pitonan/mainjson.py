from pitonan.tfidf import *
import pandas as pd
import json

def getsorted(query):

    #Membaca dbDokumen.txt untuk mendapatkan isi konten artikel
    with open('data/json/dbDokumen.txt') as fin:
        dbDokumen = json.load(fin)

    #Membaca dbArticle.txt untuk mendapatkan data berupa judul, link, dan kalimat pertama dari masing-masing artikel
    with open('data/json/dbArticle.txt') as fin:
        dbArticle = json.load(fin)

    #memasukkan hasil stemming per dokumen ke dalam list stemmed_content
    stemmed_content = [stem(dokumen) for dokumen in dbDokumen] 

    stemmed_content.append(stem(query))

    kolom_vect = setkata(stemmed_content)
    del stemmed_content[-1]


    contents_wcount = [wordcount(content, kolom_vect) for content in stemmed_content]
    idf_vect = idfvect(contents_wcount)
    #print(contents_wcount)

    vect_query = tf(wordcount(stem(query), kolom_vect))

    # Mencari cosine sim


    cos = [0 for i in range(len(dbArticle))]
    ti  = [0 for i in range(len(dbArticle))]
    tiq = tf_idf(vect_query,idf_vect)

    for i in range(len(dbArticle)):
        tfd = tf(contents_wcount[i])
        ti[i] = tf_idf(tfd,idf_vect)
        cos[i] = cosine_sim(tiq,ti[i])
        dbArticle[i].update({"similarity" : cos[i]})

    dbArticle = sorted(dbArticle, key = lambda i: i['similarity'],reverse=True)

    return dbArticle

def tablemaker(query):
    #Membaca dbDokumen.txt untuk mendapatkan isi konten artikel
    with open('data/json/dbDokumen.txt') as fin:
        dbDokumen = json.load(fin)

    #Membaca dbArticle.txt untuk mendapatkan data berupa judul, link, dan kalimat pertama dari masing-masing artikel
    with open('data/json/dbArticle.txt') as fin:
        dbArticle = json.load(fin)

    #memasukkan hasil stemming per dokumen ke dalam list stemmed_content
    stemmed_content = [stem(dokumen) for dokumen in dbDokumen] 

    stemmed_content.append(stem(query))

    kolom_vect = setkata(stemmed_content)
    del stemmed_content[-1]


    contents_wcount = [wordcount(content, kolom_vect) for content in stemmed_content]

    kolque = setkata([stem(query)])
    df = pd.DataFrame.from_records(contents_wcount)
    df = df[df.columns.intersection(list(kolque))]
    for i in range(len(dbArticle)):
        df = df.rename(index = { i : '<a href="{}">{}</a>'.format(dbArticle[i]["link"],'D'+str(i+1))})

    return df



