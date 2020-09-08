import requests
from bs4 import BeautifulSoup
import gspread
import datetime

def request():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'}
    url = 'https://www.scan.co.uk/products/2tb-samsung-860-evo-25-ssd-sata-iii-6gb-s-mjx-mlc-v-nand-2gb-cache-read-550mb-s-write-520mb-s-98k-90'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def parse(soup):
    date = datetime.datetime.now()
    name = soup.find('h1').text.strip()
    price = soup.find('div', class_ = 'leftColumn').text.strip().replace('£','')
    stock = soup.find('span', class_ = 'in stock').text.strip()
    product = {'date':date, 'name':name, 'price':price, 'stock': stock}
    return product

def output(product):
    gc = gspread.service_account(filename='creds.json')
    sh = gc.open('scrapetosheets').sheet1
    sh.append_row([str(product['date']), str(product['name']), float(product['price']), str(product['stock'])])
    return
    
data = request()
product = parse(data)
output(product)
