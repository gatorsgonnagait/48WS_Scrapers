from bs4 import BeautifulSoup
import urllib.request
import re
import Scraping_Tools as st



url = 'https://ajaxsprings.com'
manufacturer = 'Ajax Springs'
company = st.add_underscores(manufacturer)
product_df = st.create_product_df()
link = urllib.request.urlopen(url)
soup = BeautifulSoup(link.read(), "html.parser")
type_list = soup.find_all('li', {'id': re.compile(r'^menu-item-20(0[8-9])|(1[0-3)])')})


for li in type_list:
    if li.find('a') is not None:

        cat_link = li.find('a').attrs['href']
        sub_link = urllib.request.urlopen(cat_link)
        sub_soup = BeautifulSoup(sub_link, "html.parser")

        item_url = ''
        for i in sub_soup.find('ul', {'class':'wpv-pagination-nav-links-container js-wpv-pagination-nav-links-container'}):
            if i.find('a'):
                item_url = i.find('a').attrs['href'][:-1]
                break

        page_limit = int([i for i in sub_soup.find('ul', {'class': 'wpv-pagination-nav-links-container js-wpv-pagination-nav-links-container'})][-1].text)

        for i in range(1, page_limit+1):
            page_url = url + item_url + str(i)
            print(page_url)
            page_link = urllib.request.urlopen(page_url)
            item_soup = BeautifulSoup(page_link, 'html.parser')

            table = item_soup.find('tbody', {'class':'wpv-loop js-wpv-loop'})#item_soup.find_all('table', {'class': 'springTable'})
            for row in table.find_all('tr'):

                item_li = [j for j in row]
                sku = item_li[1].text
                product_df.at[sku, 'SKU #'] = sku
                product_df.at[sku, 'Product Name'] = item_li[5].text + ' '+item_li[7].text
                product_df.at[sku, 'Description'] = item_li[9].text
                product_df.at[sku, 'Manufacturer'] = item_li[5].text
                product_df.at[sku, 'Info/Size/Color'] = item_li[11].text

st.export_df(product_df, company, url)