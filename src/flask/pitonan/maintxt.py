from pathlib import Path
from pitonan.tfidf import *

def get_localcorpus():
    corpus = []
    data_folder = Path('data/txt/')
    files = data_folder.glob('*.txt')

    i = 1
    for file in sorted(files):
        doc = {
            'judul': "file" + str(i),
            'link': file.name,
        }
        with file.open() as f:
            doc['kalimat'] = f.readline(200) + '...'
        corpus.append(doc)
        i += 1
    
    return corpus

def get_localcontent(doc):
    file = Path('data/txt/' + doc['link'])
    with file.open() as f:
        content = f.read()
    return content.replace('\n', ' ')

def getsortedtxt(query):
    dbArticle = get_localcorpus()

    #memasukkan hasil stemming per dokumen ke dalam list stemmed_content
    stemmed_content = [stem(get_localcontent(dokumen)) for dokumen in dbArticle] 

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

def tablemakertxt(query):
    dbArticle = getsortedtxt(query)

    #memasukkan hasil stemming per dokumen ke dalam list stemmed_content
    stemmed_content = [stem(get_localcontent(dokumen)) for dokumen in dbArticle] 

    stemmed_content.append(stem(query))

    kolom_vect = setkata(stemmed_content)
    del stemmed_content[-1]
    contents_wcount = [wordcount(content, kolom_vect) for content in stemmed_content]
    
    kolque = setkata([stem(query)])
    quecount = [wordcount(stem(query),kolque)]
    dq = pd.DataFrame.from_records(quecount)
    df = pd.DataFrame.from_records(contents_wcount)
    df = dq.append(df, ignore_index=True)
    df = df[df.columns.intersection(list(kolque))]
    df = df.rename(index = { 0 : 'Q'})
    for i in range(1,len(dbArticle)+1):
        df = df.rename(index = { i : '<a href="{}">{}</a>'.format("/txt/"+dbArticle[i-1]["link"],'D'+str(i))})
    
    df = df.T
        
    return df

