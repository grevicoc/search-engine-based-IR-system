from bs4 import BeautifulSoup
import requests

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
        kalimatPertama = soupArtikel.find('div', attrs={'class', 'col-md-10 col-xs-12 detailNews'}).find('p').text 

        #data tiap berita dibagi menjadi judul, link, dan kalimat pertamanya lalu dimasukkin ke dict
        tempDict = {'judul':judulArtikel, 'link':linkArtikel, 'kalimat':kalimatPertama}

        listMainArticle.append(tempDict)

#fungsi untuk ngambil isi dari link
def isiKonten(link):                                
    sourceKonten = requests.get(link).text                

    soupKonten = BeautifulSoup(sourceKonten, 'html.parser')

    konten = soupKonten.find('div', attrs={'class', 'col-md-10 col-xs-12 detailNews'})
    unWantedKonten = konten.find('div', attrs={'class', 'topicRelated'})  
    unWantedKonten.extract()  

    return konten.text
    
