from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import math
import re

# TODO dibikin sampe ada fungsi akhir yang ngereturn nilai TF-IDF per kalimat,
# nilai itu yang dipake buat sort

# jadi per dokumen disimpen kayak
# {
#     link: google.com
#     tfidf: float
# }

stop_words = set(stopwords.words("english"))
stemmer = SnowballStemmer("english")

def stem(string):
    """me-return variable string setelah stemming (menghilangkan tanda baca,
    dijadikan lowercase, dan menghilangkan stopwords) dalam bentuk 
    array of tokens"""
    clean = re.sub(r'[^\w\s]','', string).lower()
    tokenized = word_tokenize(clean)
    filtered = [stemmer.stem(w) for w in tokenized if not w in stop_words]

    return filtered

def setkata(arrkalimat):
    """me return set berisi semua kata yang muncul di setiap string di str_array,
    untuk digunakan sebagai kolom vektor"""
    kolom = set()
    for string in arrkalimat:
        kolom = kolom.union(set(string))

    return kolom

def wordcount(kalimat, setkata):
    wordcount_dict = dict.fromkeys(setkata, 0)
    for word in kalimat:
        wordcount_dict[word] += 1
    return wordcount_dict

def wordcount_matx(arrkalimat):
    """mengubah tiap array dalam arrkalimat menjadi dictionary dengan key
    tiap kata dan value jumlah kemunculannya (serupa dgn vektor)"""
    keyset = setkata(arrkalimat)
    return [wordcount(kal, keyset) for kal in arrkalimat]

def tf(wordcount_vect):
    """output dict vector dengan nilai tiap kolom berupa nilai TF pada dokumen
    wordcount_vect"""
    tf_dict = dict.fromkeys(wordcount_vect.keys())
    nkata = sum(wordcount_vect.values())
    for kata in wordcount_vect.keys():
        tf_dict[kata] = wordcount_vect[kata] / nkata
    
    return tf_dict

def tf_matx(wordcount_arr):
    """output matrix dengan nilai tiap kolom berupa nilai TF dari kata tersebut
    pada dokumen masing-masing, dengan input matrix wordcount"""
    return [tf(kalimat) for kalimat in wordcount_arr]

def idfvect(wordcount_arr):
    """mereturn vector (dictionary dengan value float) dengan input 
    array vektor wordcount"""
    idfvect = dict.fromkeys(wordcount_arr[0].keys(), 0)

    for kalimat in wordcount_arr:
        for kata, count in kalimat.items():
            if (count > 0):
                idfvect[kata] += 1

    n_kalimat = len(wordcount_arr)

    for kata, count in idfvect.items():
        idfvect[kata] = math.log((1 + n_kalimat) / (1 + count)) + 1

    return idfvect

def tf_idf(tf, idf):
    res = dict.fromkeys(tf.keys())
    for kolom in res.keys():
        res[kolom] = tf[kolom] * idf[kolom]

    return res

def cosine_sim(tfidf1,tfidf2): #cosine sim dari 2 dict tfidf 
    cosinesim = 0
    c = {key : tfidf1[key] * tfidf2.get(key,0) for key in tfidf1.keys()}
    dot = sum(c.values()) 
    sq1 ={}
    sq2 ={}
    sq1 = {key: value ** 2 for key, value in tfidf1.items()}
    sq2 = {key: value ** 2 for key, value in tfidf2.items()}
    lgt = math.sqrt(sum(sq1.values())) * math.sqrt(sum(sq2.values()))
    if(lgt!=0):
        cosinesim = dot/lgt
    
    return cosinesim

    
