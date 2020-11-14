from tfidf import *
from webscraper import *


# testcorpus contoh doang, kalo banyak dokumen bisa makan memori, jadi bisa
# dibikin fungsi content(link) dari webscraping mungkin buat ngambil content nya biar
# ga harus nyimpen terus terusan, bisa juga diadain keyvalue kalimat pertama buat 
# nanti ke website

'''
testcorpus = [
    {
        "link": "test1.com",
        "content": "poop Sometimes it is better to just walk away from things and go back to them later when you’re in a better frame of mind."
    },
    {
        "link": "test2.com",
        "content": "poop He was an introvert that extroverts seemed to love."
    },
    {
        "link": "test3.com",
        "content": "poop He didn't heed the warning and it had turned out surprisingly well."
    },
    {
        "link": "test4.com",
        "content": "poop He hated that he loved what she hated about hate."
    },
    {
        "link":"test5.com",
        "content":"walk love hate zara"
    }
]
'''

query = "covid-19 vaccine"

#memasukkan hasil stemming per dokumen ke dalam list stemmed_content
stemmed_content = [stem(isiKonten(dokumen['link'])) for dokumen in listMainArticle] 

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


cos = [0 for i in range(len(listMainArticle))]
ti  = [0 for i in range(len(listMainArticle))]
tiq = tf_idf(vect_query,idf_vect)

for i in range(len(listMainArticle)):
    tfd = tf(contents_wcount[i])
    ti[i] = tf_idf(tfd,idf_vect)
    cos[i] = cosine_sim(tiq,ti[i])
    print(cos[i])
    listMainArticle[i].update({"similarity" : cos[i]})

listMainArticle = sorted(listMainArticle, key = lambda i: i['similarity'],reverse=True)
print(listMainArticle)

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






