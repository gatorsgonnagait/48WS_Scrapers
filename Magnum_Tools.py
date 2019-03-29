import Scraping_Tools as st


ext = 'shopdisplaycategories.asp'
store_url = 'https://magnumtools.com/'
manufacturer = 'Magnum Tools'
company = st.add_underscores(manufacturer)
product_df = st.create_product_df()
soup = st.create_bs4_soup(store_url+ext)


def find_item_page(item_soup, sub_cat):

    if not item_soup.find('div', {'class': 'sort_product_container'}):
        sub_cat2 = item_soup.find('h1', {'class':'global-font-color'}).text
        #print('Category')
        #print(sub_cat)
        for m in item_soup.find_all('span', {'class': 'cattitle global-font-color'}):
            print(m.find('a').text)
            link = m.find('a').attrs['href']
            find_item_page(st.create_bs4_soup(store_url+link), sub_cat2)
    else:
        print("reached item list page")
        length = len(item_soup.find('ul', {'class':'pagination'}).find_all('li'))
        if length > 1:
            limit = length
        else:
            limit = 2

        for page in item_soup.find('ul', {'class':'pagination'}).find_all('li')[:limit]:

            if length > 1:
                item_soup2 = st.create_bs4_soup(store_url+page.find('a').attrs['href'])
            else:
                item_soup2 = item_soup

            for k in item_soup2.find_all('div', {'class':'col-sm-8 col-xs-8 view_product_section'}):

                sub_item_link = k.find('h4', {'class':'global-font-color'}).find('a').attrs['href']
                sub_item_soup = st.create_bs4_soup(store_url+sub_item_link)
                li2 = [d.text for d in sub_item_soup.find_all('span', {'class': 'productinfodetails'})]
                if len(li2) >= 3:
                    sku = li2[2]
                else:
                    sku = li2[-1]

                item_pic = ''
                if  sub_item_soup.find('img', {'id':'pimage'}):
                    item_pic = sub_item_soup.find('img', {'id':'pimage'}).attrs['src']

                product_name = sub_item_soup.find('h1', {'class':'global-font-color'}).text
                print(product_name)

                details = ''
                description = ''
                if sub_item_soup.find_all('div', {'style': 'text-align: left;'}):

                    li = [t.text for t in sub_item_soup.find_all('div', {'style': 'text-align: left;'})]
                    description = st.clear_extra_spaces(li[0])
                    details = st.clear_extra_spaces(li[-1])
                elif sub_item_soup.find_all('div', {'class': 'productdesc'}):
                    description = sub_item_soup.find('div', {'class': 'productdesc'}).text
                    details = sub_item_soup.find('div', {'id': 'xproductextdesc'}).text

                product_df.at[sku, 'SKU #'] = sku
                product_df.at[sku, 'Product Name'] = product_name
                product_df.at[sku, 'Image'] = store_url+item_pic
                product_df.at[sku, 'Details'] = details
                product_df.at[sku, 'Manufacturer'] = manufacturer
                product_df.at[sku, 'Description'] = description
                product_df.at[sku, '48WS Category'] = category
                product_df.at[sku, 'Sub Category'] = sub_cat
                #print(product_df)
        print()



for i in soup.find_all('ul', {'class':'menulist'})[1]:

    category = i.find('a').text
    print(category)
    category_link = store_url+i.find('a').attrs['href']
    sub_soup = st.create_bs4_soup(category_link)
    print('recursion')
    find_item_page(sub_soup, category)
    #break



st.export_df(product_df, company, same_company=True, url=store_url, version='products')
