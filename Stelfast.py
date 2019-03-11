from bs4 import BeautifulSoup
import urllib.request
import re
import Scraping_Tools as st

url = 'https://www.stelfast.com/'
#prod_ext = 'auto.html'
#prod_ext = 'industrial.html'
prod_ext = 'metrics.html'
manufacturer = 'Stelfast'

company = st.add_underscores(manufacturer)
product_df = st.create_product_df()
link = urllib.request.urlopen(url + prod_ext).read()
soup = BeautifulSoup(link, "html.parser")

#print(soup.find('tbody'))

for i in soup.find_all('tr'):
    print([j.text for j in i.find_all('th')])
    li = [j.text for j in i.find_all('th')]

    category = li[0]
    name = li[1] +' '+ li[2] +' '+ li[4]

    product_df.at[name, 'Category'] = category
    product_df.at[name, 'SKU #'] = name
    product_df.at[name, 'Product Name'] = name
    # product_df.at[sku, 'Info/Size/Color'] = item_li[5].text


st.export_df(product_df, company, url, same_company=True)