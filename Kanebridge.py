from bs4 import BeautifulSoup
import urllib.request
import re
import Scraping_Tools as st


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

    url = 'https://www.kanebridge.com/'
    prod_ext = '/kaneprls.asp'
    manufacturer = 'Kanebridge'
    company = st.add_underscores(manufacturer)
    product_df = st.create_product_df()
    link = urllib.request.urlopen(url+prod_ext).read()
    soup = BeautifulSoup(link, "html.parser")


    for i in soup.find_all('h5'):
        sub_cat = url + i.find('a').attrs['href']
        print(i.find('a').text, sub_cat)
        sub_link = urllib.request.urlopen(sub_cat.replace(' ', '')).read()
        sub_soup = BeautifulSoup(sub_link, "html.parser")

        for n in sub_soup.find_all('a', {'name':re.compile(r'^level_')}, href=True):
            if n.attrs['href'] and n.attrs['href'] != 'javascript:void(0)':
                item_url = url + n.attrs['href']
                name = n.text
                item_link = urllib.request.urlopen(item_url).read()
                item_soup = BeautifulSoup(item_link, "html.parser")
                table = item_soup.find('table', {'class': 'table table-striped fixed_header'})
                product_df = scrape_table(name, product_df, table)


        for j in sub_soup.find_all('p', {'class':'product-link'}):
            print(j.text)
            item_url = url + j.find('a').attrs['href']
            item_url = item_url.replace(' ', '')
            str_num = ''
            for c in reversed(item_url):
                if c == '_':
                    break
                str_num = c+str_num
            num = int(str_num)

            name = sub_soup.find('a', {'name':'level_'+str(num-1)}).text
            print(name, item_url, num)
            item_link = urllib.request.urlopen(item_url).read()
            item_soup = BeautifulSoup(item_link, "html.parser")

            if item_soup.find('table', {'class': 'table table-striped fixed_header'}):
                table = item_soup.find('table', {'class': 'table table-striped fixed_header'})
                product_df = scrape_table(name, product_df, table)


        #break

    st.export_df(product_df, company, url, same_company=True)