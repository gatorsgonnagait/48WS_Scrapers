from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
from Scraping_Tools import download_image, render_page
import os.path as path



url = 'https://www.ingersollrandproducts.com'
type = '/en-us/power-tools'
end = '.html'

product_df = pd.DataFrame(columns=['48WS.com URL','Category','SKU #','Product Name','Image','Manufacturer_URL','Weight','Manufacturer','Description','Quick Overview','Details','Group Name','Info/Size/Color','UPC'])
product_df.index.name = 'sku'

link = urllib.request.urlopen(url + type+end)
soup = BeautifulSoup(link.read(), "html.parser")
type_list = soup.find_all('div', {'class':'col-md-3 col-md-offset-1'})[1].find_all('li')#.find_all('a')
company = 'Ingersoll_Rand'

for li in type_list:
    sub_type = li.find('a').attrs['href']
    print(url + sub_type)
    sub_link = render_page(url + sub_type)#urllib.request.urlopen(url + sub_type)
    sub_soup = BeautifulSoup(sub_link, "html.parser")
    category = sub_soup.find('div', {'class': 'title'}).text
    grid = sub_soup.find_all('div', {'class':'results--part__info'})

    for i in grid:
        product_url = url + i.find('a').attrs['ng-href']
        prod_link = urllib.request.urlopen((product_url))
        product_soup = BeautifulSoup(prod_link.read(), 'html.parser')

        img_url = ''
        if product_soup.find('img', {'class': 'superSlider__img lazyload'}) is not None:
            img_url = url + product_soup.find('img', {'class': 'superSlider__img lazyload'}).attrs['data-src']

        product_name = product_soup.find('div', {'class': 'title visible-xs'}).h1.text
        post_content = product_soup.find('div', {'class': 'text-collapse-short'}).text
        manufacturer = product_soup.find('html').attrs['data-sitename']
        sku_line = product_soup.find('tbody', {'id': 'scrollSyncRight'})

        sku_set = set()
        if sku_line:
            for li, i in enumerate(sku_line.find_all('tr')):
                if sku_line.find_all('tr')[li].find_all('td')[0].text:
                    sku_set.add(sku_line.find_all('tr')[li].find_all('td')[0].text)
        elif product_soup.find('div', {'class': 'title visible-xs'}).h2 is not None:
            sku_set.add(product_soup.find('div', {'class': 'title visible-xs'}).h2.text)
        else:
            continue

        for sku in sku_set:
            product_df.at[sku, 'Category'] = category
            product_df.at[sku, 'SKU #'] = sku
            product_df.at[sku, 'Product Name'] = product_name
            product_df.at[sku, 'Image'] = img_url
            product_df.at[sku, 'Quick Overview'] = post_content
            product_df.at[sku, 'Manufacturer'] = manufacturer

            print(sku, product_name)
        print(img_url)
        download_image(company, img_url)

        #break
    #break
product_df['48WS.com URL'] = 'http://www.48ws.com/'
product_df['Manufacturer_URL'] = url
product_df.to_excel(company+path.sep+company+'_products.xlsx', index=False)
