import requests
from bs4 import BeautifulSoup
from time import sleep
import sqlite3

# Konstantos
URL = 'http://quotes.toscrape.com'
conn = sqlite3.connect('quotes.db')
c = conn.cursor()

# Lentelės sukūrimas


def make_database():
    query = '''
    CREATE TABLE IF NOT EXISTS quotes(
        quote TEXT,
        author TEXT,
        hint1 TEXT,
        hint2 TEXT
    )
    '''
    with conn:
        c.execute(query)


def make_initials(name):
    '''
    funkcija, kuri iš paduoto teksto suformuoja inicialus
    '''
    splitted = name.split()
    hint = ''
    for i in splitted:
        if '.' not in i:
            hint += f'{i[0]}.'
        else:
            hint += i
    return hint


def get_hint2(endpoint):
    '''
    funkcija, kuri paduotą endpointą prideda prie URL ir ištraukia antrą užuominą
    '''
    r = requests.get(URL + endpoint)
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.select('p')[1].get_text()
    return text


def get_page(page):
    r = requests.get(URL + '/page/' + str(page)).text
    soup = BeautifulSoup(r, 'html.parser')
    quotes = soup.select('.quote')
    res = []
    for i in quotes:
        quote = i.find(class_='text').get_text()
        author = i.find(class_='author').get_text()
        hint1 = make_initials(author)
        link = i.find('a', attrs={'class': None}).get('href')
        hint2 = get_hint2(link)
        sleep(0.2)
        res.append((quote, author, hint1, hint2))
    return res

def clear_database():  #sukuriu funkciją, kuri ištrina viską iš DB, tam, kad nesidubliuotų įrašai ir visada būtų tik 100
    with conn:
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='quotes'")
        table_exists = c.fetchone()
        if table_exists: #IF reikalingas pirmąkart paleidžiant DB, kai dar nėra sukurta lentelė QUOTES, kad išvengtume klaidos. 
            c.execute('DELETE FROM quotes')
        else:
            return
        
        
clear_database()


big_list = []
for i in range(10):
    big_list += get_page(str(i + 1))




make_database()
with conn:
    c.executemany('INSERT INTO quotes VALUES (?,?,?,?)', big_list)
