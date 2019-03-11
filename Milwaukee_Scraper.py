from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import numpy as np
import os.path as path

company = 'Milwaukee'
product_numbers = pd.read_excel(company+path.sep+company+'_products_old.xlsx')
file_path = company + path.sep

if company == 'Milwaukee':
    site_url = 'https://www.milwaukeetool.com'
    product_url = 'https://www.milwaukeetool.com/Products/'
    img_class = 'media-gallery__img'
    description_class = 'product-info__overview readmore'

product_df = pd.DataFrame()


for i in product_numbers.index:
    print(product_numbers.at[i, 'sku'])
    link = urllib.request.urlopen(product_url+product_numbers.at[i, 'sku'])
    soup = BeautifulSoup(link.read(), "html.parser")

    if soup.find('div', {description_class}) is not None:
        post_content_div = soup.find('div', {'class': description_class}).find_all('p')
        post_title = soup.find('h1', {'class':'product-info__title'}).text
        img_url = soup.find('div', {'class':img_class}).find('img').get('src')

        if company == 'Milwaukee':
            img_url = site_url + img_url

        clean = img_url.replace('"', '')
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

        urllib.request.urlretrieve(img_url, file_path+'pics'+path.sep+clean+'.png')

        if company == 'Makita':
            post_content = ''
            for line in post_content_div:
                post_content += line.text
        elif company == 'Milwaukee':
            post_content = post_content_div[0].text

        product_numbers.at[i, 'post_title'] = post_title
        product_numbers.at[i, 'Image'] = post_title+'.png'
        product_numbers.at[i, 'post_content'] = post_content


    print()

product_numbers.to_excel(company+path.sep+company+'_products.xlsx', index=False)