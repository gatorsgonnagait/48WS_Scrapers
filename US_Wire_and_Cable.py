import Scraping_Tools as st
from bs4 import BeautifulSoup
import re
import urllib.request
import bs4


url = 'http://uswireandcable.com/'
prod_ext = 'products.html'
manufacturer = 'US Wire and Cable'
company = st.add_underscores(manufacturer)
product_df = st.create_product_df()

soup = st.create_bs4_soup(url+prod_ext)



for i in soup.find_all('a', href=True)[6:-1]:
    print(i.attrs['href'])
    print(i.find('img').attrs['src'])

    img = url + i.find('img').attrs['src']
    sub_url = url + i.attrs['href']
    sub_soup = st.create_bs4_soup(sub_url)

    category = sub_soup.find('h2').text
    print(category)
    print()

    for names, table, desc in zip(sub_soup.find_all(re.compile('h3'))[1:], sub_soup.find_all('table')[2:-1],  [li for li in sub_soup.find_all('p')[4:-1] if st.clear_extra_spaces(st.clear_extra_spaces(li.text))]) :
        print(names.text)
        name = names.text
        description = st.clear_extra_spaces(desc.text)
        print(description)


        print()



st.export_df(product_df, company, url, same_company=True, version='with_products')
