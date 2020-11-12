from bs4 import BeautifulSoup
import requests

source = requests.get('https://www.kompasiana.com/tag/2020').text

soup = BeautifulSoup(source, 'html.parser')

artikel_raw = soup.find('div', {'id':'index_tag'})     #ini dia cuma bakal nemuin container utamanya dan disimpan di variable artikel_raw

konten_artikel = artikel_raw.find_all('div', attrs={'class', 'timeline--item'})     #jadi bisa dibilang artikel_raw itu kayak container utama, dan di sini kita masukkin masing-masing konten dari container utama itu ke list konten_artikel

list_of_artikel = []

for konten in konten_artikel:
    penulis_artikel = konten.find('div', attrs={'class', 'user-box col-lg-12 col-md-12 col-sm-12 col-xs-12'}).find('a').text

    tanggal_artikel = konten.find('div', attrs={'class', 'user-box col-lg-12 col-md-12 col-sm-12 col-xs-12'}).find('div').text
    
    konten_artikel = konten.find('h2').find('a').get('href')    

    tempDict = {'penulis' : penulis_artikel, 'tanggal artikel' : tanggal_artikel, 'link' : konten_artikel}

    list_of_artikel.append(tempDict)

def isiKonten(link):                                #fungsi untuk ngambil isi dari link
    source = requests.get(link).text                

    soup = BeautifulSoup(source, 'html.parser')

    konten = soup.find('div', attrs={'class', 'read-content'}).find_all('p')        #di sini kita ambil semua isi konten dari link tersebut dengan cara semua tag html <p> diambil dan disimpan di konten

    for  paragraf in konten:                        #setelah itu, karena tiap index di konten menandakan dia paragraf ke berapa, makanya gue buat loop biar nanti bisa diatur per paragraf
        print(paragraf.text + '\n')

isiKonten(list_of_artikel[0]['link'])