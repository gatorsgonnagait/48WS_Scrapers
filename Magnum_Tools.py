import Scraping_Tools as st
from bs4 import BeautifulSoup
import re
from selenium import webdriver


ext = 'shopdisplaycategories.asp'
store_url = 'https://magnumtools.com/'
manufacturer = 'Magnum Tools'
company = st.add_underscores(manufacturer)
product_df = st.create_product_df()
print(store_url+ext)
soup = st.create_bs4_soup(store_url+ext)


def find_item_page(item_soup):

    if not item_soup.find('div', {'class': 'sort_product_container'}):
        sub_cat = item_soup.find('h1', {'class':'global-font-color'}).text
        print('Category')
        print(sub_cat)
        for m in item_soup.find_all('span', {'class': 'cattitle global-font-color'}):
            print(m.find('a').text)
            link = m.find('a').attrs['href']

            sub_soup = st.create_bs4_soup(store_url+link)
            find_item_page(sub_soup)
    else:

        print("reached item list page")
        for page in item_soup.find_all():
            pass
        # figure out pagination
        for k in item_soup.find_all('div', {'class':'col-sm-8 col-xs-8 view_product_section'}):



            sub_item_link = k.find('h4', {'class':'global-font-color'}).find('a').attrs['href']
            #print(sub_item_link)

            sub_item_soup = st.create_bs4_soup(store_url+sub_item_link)


            li2 = [d.text for d in sub_item_soup.find_all('span', {'class': 'productinfodetails'})]
            sku = li2[2]

            item_pic = sub_item_soup.find('img', {'id':'pimage'}).attrs['src']
            #print(item_pic)
            product_name = sub_item_soup.find('h1', {'class':'global-font-color'}).text
            print(product_name)
            li = [t.text for t in sub_item_soup.find_all('div', {'style': 'text-align: left;'})]
            description = st.clear_extra_spaces(li[0])
            details = st.clear_extra_spaces(li[1])

            product_df.at[sku, 'SKU #'] = sku
            product_df.at[sku, 'Product Name'] = product_name
            product_df.at[sku, 'Image'] = store_url+item_pic
            product_df.at[sku, 'Details'] = details
            product_df.at[sku, 'Manufacturer'] = manufacturer
            product_df.at[sku, 'Description'] = description
            product_df.at[sku, '48WS Category'] = category

        print()
        return


for i in soup.find_all('ul', {'class':'menulist'})[1]:
    #if i.find('li') is not None:

    #print(i.find('a').text, i.find('a').attrs['href'])

    category = i.find('a').text
    print(category)
    category_link = store_url+i.find('a').attrs['href']
    #print(category_link)
    sub_soup = st.create_bs4_soup(category_link)
    #print(sub_soup)
    print('recursion')
    find_item_page(sub_soup)

    # for j in sub_soup.find_all('span', {'class':'cattitle global-font-color'}):
    #
    #     print(j.find('a').text)
    #     sub_link = j.find('a').attrs['href']
    #     #print(store_url+sub_link)
    #     item_soup = st.create_bs4_soup(store_url+sub_link)
    #     print('recrusion')
    #     find_item_page(item_soup)



        #if item_soup.find('div', {'class':'sort_product_container'}):
            # for k in item_soup.find_all('div', {'class':'col-sm-8 col-xs-8 view_product_section'}):
            #
            #     sub_item_link = k.find('h4', {'class':'global-font-color'}).find('a').attrs['href']
            #     #print(sub_item_link)
            #     sub_item_soup = st.create_bs4_soup(store_url+sub_item_link)
            #
            #
            #     li2 = [d.text for d in sub_item_soup.find_all('span', {'class': 'productinfodetails'})]
            #     sku = li2[2]
            #
            #     item_pic = sub_item_soup.find('img', {'id':'pimage'}).attrs['src']
            #     #print(item_pic)
            #     product_name = sub_item_soup.find('h1', {'class':'global-font-color'}).text
            #     print(product_name)
            #     li = [t.text for t in sub_item_soup.find_all('div', {'style': 'text-align: left;'})]
            #     description = st.clear_extra_spaces(li[0])
            #     details = st.clear_extra_spaces(li[1])
            #
            #     product_df.at[sku, 'SKU #'] = sku
            #     product_df.at[sku, 'Product Name'] = product_name
            #     product_df.at[sku, 'Image'] = store_url+item_pic
            #     product_df.at[sku, 'Details'] = details
            #     product_df.at[sku, 'Manufacturer'] = manufacturer
            #     product_df.at[sku, 'Description'] = description
            #     product_df.at[sku, '48WS Category'] = category


    break

    #break

st.export_df(product_df, company, same_company=True, url=store_url, version='products')
