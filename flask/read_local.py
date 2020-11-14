from pathlib import Path
import os

def get_localcorpus():
    corpus = []
    data_folder = Path('data/')
    files = data_folder.glob('*.txt')

    i = 1
    for file in sorted(files):
        doc = {
            'judul': "file" + str(i),
            'link': file.name,
        }
        with file.open() as f:
            doc['kalimat'] = f.readline(100) + '...'
        corpus.append(doc)
        i += 1
    
    return corpus

def get_localcontent(doc):
    file = Path('data/' + doc['link'])
    with file.open() as f:
        content = f.read()
    return content.replace('\n', ' ')