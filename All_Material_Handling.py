from bs4 import BeautifulSoup
import urllib.request
import re
import Scraping_Tools as st
import os.path as path


url = 'http://allmaterialhandling.com/#'
company = 'All_Material_Handling'
manufacturer = st.clean_punctuation(company)
product_df = st.create_product_df()
link = urllib.request.urlopen(url)
soup = BeautifulSoup(link.read(), "html.parser")
type_list = soup.find('div', {'class': 'fusion-main-menu'}).find_all('a')#.attrs['href']

for c, li in enumerate(type_list):

    if ( c > 0 and  c < 15) or c == 21 or c == 24:
        sub_link = urllib.request.urlopen(li.attrs['href'])
        sub_soup = BeautifulSoup(sub_link, "html.parser")
        product_name = sub_soup.find('h1', {'class': 'entry-title'}).text
        table = sub_soup.find_all('td', {'class':'column-1'})
        img_url = ''
        if sub_soup.find('img', {'class': re.compile(r'^alignnone wp-image-')})is not None:
            img_url = sub_soup.find('img', {'class': re.compile(r'^alignnone wp-image-')}).attrs['src']

        description = sub_soup.find_all('div', {'class': 'fusion-column-wrapper'})
        text = ''
        for li in description[0].find_all('li'):
            text += li.text+'. '

        print(text)
        print(manufacturer)
        for i, sku in enumerate(table):
            if i > 0:
                product_df.at[sku.text, 'SKU #'] = sku.text
                product_df.at[sku.text, 'Product Name'] = product_name
                product_df.at[sku.text, 'Image'] = img_url
                product_df.at[sku.text, 'Details'] = text
                product_df.at[sku.text, 'Manufacturer'] = manufacturer

product_df['48WS.com URL'] = 'http://www.48ws.com/'
product_df['Manufacturer_URL'] = url
product_df.to_excel(company+path.sep+company+'_products.xlsx', index=False)
