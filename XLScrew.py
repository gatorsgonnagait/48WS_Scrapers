import Scraping_Tools as st
from bs4 import BeautifulSoup
import urllib.request


def scrape_table(name, product_df, table):

    for row in table.find_all('tr'):
        if row.find_all('td'):
            item_li = [j for j in row.find_all('td')]
            sku = item_li[0].text
            print(name)
            print(item_li[0].text, item_li[1].text, item_li[5].text)
            product_df.at[sku, 'SKU #'] = sku
            product_df.at[sku, 'Product Name'] = name
            product_df.at[sku, 'Info/Size/Color'] = item_li[5].text

    return product_df




if __name__ == '__main__':

    url = 'https://www.xlscrew.com'
    prod_ext = '/stock-catalogs/'
    manufacturer = 'XL Screw'
    company = st.add_underscores(manufacturer)
    product_df = st.create_product_df()
    link = urllib.request.urlopen(url + prod_ext).read()
    soup = BeautifulSoup(link, "html.parser")


    for i in soup.find_all('a', {'class':'thumb-block animsition-link'}):
        sub_url = i.attrs['href']
        sub_cat = i.attrs['title']
        sub_link = urllib.request.urlopen(sub_url.replace(' ', '')).read()
        sub_soup = BeautifulSoup(sub_link, "html.parser")
        for j, k, p in zip(sub_soup.find_all('p'), sub_soup.find_all('tbody'), sub_soup.find_all('a', {'class':'magnific'})):
            name = j.text
            print(name)
            count = 0
            img = p.attrs['href']
            for row in k.find_all('tr'):

                li = [l for l in row.find_all('td')]
                sku = name + '_' + str(count)
                product_df.at[sku, 'SKU #'] = sku
                product_df.at[sku, 'Product Name'] = name
                product_df.at[sku, 'Description'] = li[0].text
                product_df.at[sku, 'Info/Size/Color'] = li[1].text
                product_df.at[sku, 'Weight'] = li[2].text
                product_df.at[sku, 'Image'] = img
                product_df.at[sku, '48WS Category'] = sub_cat
                count+=1


    st.export_df(product_df, company, url, same_company=True)