from tfidf import *

# testcorpus contoh doang, kalo banyak dokumen bisa makan memori, jadi bisa
# dibikin fungsi content(link) dari webscraping mungkin buat ngambil content nya biar
# ga harus nyimpen terus terusan, bisa juga diadain keyvalue kalimat pertama buat 
# nanti ke website
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
    }
]

def tf_idf(tf, idf):
    res = dict.fromkeys(tf.keys())
    for kolom in res.keys():
        res[kolom] = tf[kolom] * idf[kolom]

    return res



query = "walk love hate zara"

stemmed_content = [stem(dokumen["content"]) for dokumen in testcorpus]

stemmed_content.append(stem(query))
kolom_vect = setkata(stemmed_content)
del stemmed_content[-1]

contents_wcount = [wordcount(content, kolom_vect) for content in stemmed_content]
idf_vect = idfvect(contents_wcount)

vect_query = tf(wordcount(stem(query), kolom_vect))
print(idf_vect)
print(tf_idf(vect_query, idf_vect))

# TODO nanti tiap dokumen di testcorpus dibuat tf_idf dan diitung cosine sim nya
# yang dibandingin sama vect_query, baru nilai cosine sim itu dijadiin data di dalem
# dictionary tiap dokumen, dari data itu di sort