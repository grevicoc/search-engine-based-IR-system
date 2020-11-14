from tfidf import *
from read_local import *


# testcorpus contoh doang, kalo banyak dokumen bisa makan memori, jadi bisa
# dibikin fungsi content(link) dari webscraping mungkin buat ngambil content nya biar
# ga harus nyimpen terus terusan, bisa juga diadain keyvalue kalimat pertama buat 
# nanti ke website

query = "good answer"

corpus = get_localcorpus()
#memasukkan hasil stemming per dokumen ke dalam list stemmed_content
stemmed_content = [stem(get_localcontent(dokumen)) for dokumen in corpus] 

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

# Testing cosinesim


cos = [0 for i in range(len(corpus))]
ti  = [0 for i in range(len(corpus))]
tiq = tf_idf(vect_query,idf_vect)

for i in range(len(corpus)):
    tfd = tf(contents_wcount[i])
    ti[i] = tf_idf(tfd,idf_vect)
    cos[i] = cosine_sim(tiq,ti[i])
    corpus[i].update({"similarity" : cos[i]})

corpus = sorted(corpus, key = lambda i: i['similarity'],reverse=True)
for doc in corpus:
    print(doc['similarity'])

kolque = setkata([stem(query)])
df = pd.DataFrame.from_records(contents_wcount)
df = df[df.columns.intersection(list(kolque))]
df = df
print(df.rename(index=lambda s:'D'+str(s)))
