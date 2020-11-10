from bs4 import BeautifulSoup
import requests

source = requests.get('https://www.kompasiana.com/tag/2020').text

soup = BeautifulSoup(source, 'html.parser')

artikel_raw = soup.find('div', {'id':'index_tag'})     #ini dia cuma bakal nemuin container utamanya dan disimpan di variable artikel_raw

konten_artikel = artikel_raw.find_all('div', attrs={'class', 'timeline--item'})     #jadi bisa dibilang artikel_raw itu kayak container utama, dan di sini kita masukkin masing-masing konten dari container utama itu ke list konten_artikel

for konten in konten_artikel:
    penulis_artikel = konten.find('div', attrs={'class', 'user-box col-lg-12 col-md-12 col-sm-12 col-xs-12'}).find('a').text

    tanggal_artikel = konten.find('div', attrs={'class', 'user-box col-lg-12 col-md-12 col-sm-12 col-xs-12'}).find('div').text
    
    konten_artikel = konten.find('h2').find('a').get('href')    #ini baru sampe tahap kita dapetin masing-masing link artikel kedepannya sih tinggal diulang aja caranya, nanti gue lanjut

    print(penulis_artikel + '\n' + tanggal_artikel + '\n' + konten_artikel + '\n')
    
'''
contoh hasilnya:
Agung Gumelar Ansori
10 November 2020 | 2 jam lalu
https://www.kompasiana.com/agunggumela8765/5faa9e8ed541df5b8c724132/selamat-ya-joe-biden-dan-kamala-harris-menang-gokil-dahh

Shafira Azzahra
10 November 2020 | 8 jam lalu
https://www.kompasiana.com/safirasunmi86/5faa414d8ede487a66517a42/kapan-sadarnya-ekhem-mba-mas-semester-7

sekar ardya wardhani
07 November 2020 | 3 hari lalu
https://www.kompasiana.com/sekar36615/5fa65dfad541df674f0d8642/trump-vs-biden-siapakah-yang-akan-menang
    '''
    