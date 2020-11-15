from tfidf import *
import json

query = "covid-19 vaccine"

#Membaca dbDokumen.txt untuk mendapatkan isi konten artikel
with open('flask/data/json/dbDokumen.txt') as fin:
    dbDokumen = json.load(fin)

#Membaca dbArticle.txt untuk mendapatkan data berupa judul, link, dan kalimat pertama dari masing-masing artikel
with open('flask/data/json/dbArticle.txt') as fin:
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

kolque = setkata([stem(query)])
df = pd.DataFrame.from_records(contents_wcount)
df = df[df.columns.intersection(list(kolque))]
df = df.rename(index=lambda s:'D'+str(s))
print(df)
html = '''
<html>
  <head><title>HTML Pandas Dataframe with CSS</title></head>
  <link rel="stylesheet" type="text/css" href="df_style.css"/>
  <body>
    {table}
  </body>
</html>.
'''
pd.set_option('colheader_justify', 'center')
text_file = open("pup.html", "w")
text_file.write(html.format(table=df.to_html(classes='mystyle')))
text_file.close()






