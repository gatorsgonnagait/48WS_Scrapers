import Scraping_Tools as st
from bs4 import BeautifulSoup
import re
import urllib.request


url = 'http://phd-mfg.com'
prod_ext = '/product/'
manufacturer = 'PhD Manufacturing'
company = st.add_underscores(manufacturer)
product_df = st.create_product_df()

link = urllib.request.Request(url + prod_ext, headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
html = urllib.request.urlopen(link)
soup = BeautifulSoup(html.read(), "html.parser")




for i in soup.find_all('li', {'class': re.compile(r'^product-category')}):
    sub_url = i.find('a').attrs['href']
    sub_link = urllib.request.Request(sub_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
    html2 = urllib.request.urlopen(sub_link)
    sub_soup = BeautifulSoup(html2.read(), "html.parser")

    for j in sub_soup.find_all('li', {'class': re.compile(r'^product-category')}):
        prod_url = j.find('a').attrs['href']
        print(prod_url)
        category = j.find('img').attrs['alt']

        sub_link2 = urllib.request.Request(prod_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
        html3 = urllib.request.urlopen(sub_link2)
        sub_soup2 = BeautifulSoup(html3.read(), "html.parser")

        for k, l in zip(sub_soup2.find_all('div', {'id':'product-loop-content'}), sub_soup2.find_all('img', {'class':re.compile('attachment-')} ) ) :
            print(k.find('a').text)
            name = k.find('a').text
            description = k.find_all('p')[-1].text
            img = l.attrs['src']
            line = k.find('p').text[8:].replace('&', '')#.replace[',', '']
            line = line.replace(',', '')
            line = line.replace('-', '')

            for sku in line.split():
                print(sku)
                product_df.at[sku, 'SKU #'] = sku
                product_df.at[sku, 'Product Name'] = name
                product_df.at[sku, 'Description'] = description
                product_df.at[sku, 'Image'] = img
                product_df.at[sku, '48WS Category'] = category
            print()

st.export_df(product_df, company, url, same_company=True)