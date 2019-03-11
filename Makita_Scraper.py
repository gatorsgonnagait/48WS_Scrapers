from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import numpy as np
import os.path as path

company = 'Makita'
product_numbers = pd.read_excel('products.xlsx')
file_path = company + path.sep

product_df = pd.DataFrame()


for i in product_numbers.index:
    print(product_numbers.at[i, 'sku'])
    link = urllib.request.urlopen('https://www.makitatools.com/products/details/'+product_numbers.at[i, 'sku'])
    soup = BeautifulSoup(link.read(), "html.parser")

    if soup.find('div', {'class':'row detail-section detail-about js-expand'}) is not None:
        post_content_div = soup.find('div', {'class': 'row detail-section detail-about js-expand'}).find_all('p')
        post_title = soup.find('div', {'class':'prod-description'}).text
        img_url = soup.find('div', {'class':'dyn-modal-win'}).find('img').get('src')
        clean = post_title.replace('"', '')
        clean = clean.replace('.', '')
        clean = clean.replace('\\', '')
        clean = clean.replace('/', '')
        clean = clean.replace('*', '')
        clean = clean.replace('|', '')
        clean = clean.replace(':', '')
        clean = clean.replace('<', '')
        clean = clean.replace('>', '')
        clean = clean.replace('?', '')
        print(clean)

        urllib.request.urlretrieve(img_url, file_path+clean+'.png')

        post_content = ''
        for line in post_content_div:
            #print(line.text)
            post_content += line.text

        product_numbers.at[i, 'post_title'] = post_title
        product_numbers.at[i, 'Image'] = post_title+'.jpg'
        product_numbers.at[i, 'post_content'] = post_content

    print()

product_numbers.to_excel(company+'_products.xlsx', index=False)