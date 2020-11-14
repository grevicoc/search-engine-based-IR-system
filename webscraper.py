from bs4 import BeautifulSoup
import requests
import json

listMainArticle = []

#Source Webscraping 1: Jakarta Post dengan cakupan SE Asia
source1 = requests.get('https://www.thejakartapost.com/seasia').text

soupJakartaPost1 = BeautifulSoup(source1, 'html.parser')

#Source Webscraping 2: Jakarta Post dengan cakupan Dunia
source2 = requests.get('https://www.thejakartapost.com/news/world').text

soupJakartaPost2 = BeautifulSoup(source2, 'html.parser')

#membuat list berisi masing-masing berita

listOfArticleJakartaPost = soupJakartaPost1.find_all('div', attrs={'class', 'listNews whtPD columns'})              

listOfArticleJakartaPost.extend(soupJakartaPost2.find_all('div', attrs={'class', 'listNews whtPD columns'}))

for article in listOfArticleJakartaPost:
    
    #ekstrak judul
    judulArtikel = article.find('h2', attrs={'class', 'titleNews'})
    unWantedTitle = judulArtikel.find('div')        #karena di beberapa judul ada kata PREMIUM dan dia hanya bisa diakses kalo punya akun, makanya berita yang PREMIUM di bawah ga gue masukkin
    if not unWantedTitle:
        #ekstrak link
        linkArtikel = article.find('div', attrs={'class', 'imageNews'}).find('a').get('href')

        #ekstrak kalimat pertama
        sourceArtikel = requests.get(linkArtikel).text
        soupArtikel = BeautifulSoup(sourceArtikel, 'html.parser')
        kalimatPertama = soupArtikel.find('div', attrs={'class', 'col-md-10 col-xs-12 detailNews'}).find('p')

        #data tiap berita dibagi menjadi judul, link, dan kalimat pertamanya lalu dimasukkin ke dict
        tempDict = {'judul':judulArtikel.text.strip(), 'link':linkArtikel, 'kalimat':kalimatPertama.text}       #.text untuk mengextract bagian berisi text dari tag element, sedangkan .strip untuk menghilangkan \n pada hasil extract text

        listMainArticle.append(tempDict)


#fungsi untuk ngambil isi dari link
def isiKonten(link):                                
    sourceKonten = requests.get(link).text                

    soupKonten = BeautifulSoup(sourceKonten, 'html.parser')

    konten = soupKonten.find('div', attrs={'class', 'col-md-10 col-xs-12 detailNews'})
    unWantedKonten = konten.find('div', attrs={'class', 'topicRelated'})  
    if unWantedKonten:
        unWantedKonten.extract()

    return konten.text

mainDokumen = [isiKonten(dokumen['link']) for dokumen in listMainArticle]


#Untuk meminimalisasi waktu, kami simpan konten tiap artikel ke dalam dbDokumen.txt
with open('dbDokumen.txt', 'w') as fout:       
    json.dump(mainDokumen, fout)

#Sedangkan list of dict dari data tiap artikelnya disimpan ke dalam dbArticle.txt 
with open('dbArticle.txt', 'w') as fout:
    json.dump(listMainArticle, fout)    
    
