from bs4 import BeautifulSoup
import urllib.request
import re
import Scraping_Tools as st
import os.path as path


url = 'https://www.inweldcorporation.com'
manufacturer = 'Inweld'
company = st.add_underscores(manufacturer)
product_df = st.create_product_df()
link = urllib.request.urlopen(url)
soup = BeautifulSoup(link.read(), "html.parser")
type_list = soup.find_all('ul', {'id': 'menu'})[0]#.find_all('a')#.attrs['href']

for c, li in enumerate(type_list.find_all('a')):
    if c > 0:

        product_url = url + li.attrs['href']
        print(product_url)
        sub_link = urllib.request.urlopen(product_url)
        sub_soup = BeautifulSoup(sub_link, "html.parser")
        # print(sub_soup.prettify())
        if sub_soup.find('div', {'class':'categories'}) is None:
            continue
        container = sub_soup.find('div', {'class':'categories'})
        #
        #print(container)
        url_set = set()
        for item in container.find_all('a'):
            #print(item.attrs['href'])
            item_url = url + item.attrs['href']


            if item_url not in url_set:
                print(item_url)
                url_set.add(item_url)
                item_link =  urllib.request.urlopen(item_url)
                item_soup = BeautifulSoup(item_link, "html.parser")
                #print(item_soup)
                title = item_soup.find_all('div', {'class': re.compile(r'^category_header')})

                img_url = ''
                if item_soup.find_all('img')[1].attrs['src'] is not None:
                    img_url = item_soup.find_all('img')[1].attrs['src']
                    if img_url is not None:
                        img_url = url + img_url
                    else:
                        img_url = ''

                base_product_name = ''
                sku= ''
                for i in title:
                    print(i.h1.text)
                    base_product_name += i.h1.text


                grid = item_soup.find('tbody', {'id':'infinite_scroll'})#item_soup.find_all('table')
               # print(table.find_all('a', href=True))

                if grid:
                    #pass
                    for c, l in enumerate(grid.find_all('tr')):
                        sku = l.text.strip().split()[0]
                        print(sku)
                        product_df.at[sku, 'SKU #'] = sku
                        product_df.at[sku, 'Product Name'] = base_product_name
                        product_df.at[sku, 'Image'] = img_url

                else:
                    for c, l in enumerate(item_soup.find_all('div', {'class':'title'})):
                        #pass
                        #print(l.text.strip().split()[0], l.text.strip().split()[1:])
                        sku = l.text.strip().split()[0]
                        product_name = ' '.join(l.text.strip().split()[1:])
                        print(sku, product_name)
                        product_df.at[sku, 'SKU #'] = sku
                        product_df.at[sku, 'Product Name'] = product_name
                        product_df.at[sku, 'Image'] = img_url




product_df['48WS.com URL'] = 'http://www.48ws.com/'
product_df['Manufacturer_URL'] = url
product_df.to_excel(company+path.sep+company+'_products.xlsx', index=False)