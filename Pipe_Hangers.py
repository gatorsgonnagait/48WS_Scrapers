import Scraping_Tools as st
from bs4 import BeautifulSoup
import re
from selenium import webdriver


ext = '/storefrontCommerce/'
store_url = 'https://storefront.pipehangers.com'
prod_ext = 'products.html'
manufacturer = 'Pipe Hangers'
driver = webdriver.Chrome()
company = st.add_underscores(manufacturer)
product_df = st.create_product_df()
driver.get(store_url)
page = driver.page_source
soup = BeautifulSoup(page, "html.parser")

current_cat_no = 0
page_limit = 50
for k, j in enumerate(soup.find_all('div', {'id':re.compile(r'^withsubcategories')})):
    print(j.text)
    #print(k)
    sub_url = store_url+j.find('a').attrs['href']
    driver.get(sub_url)
    driver.refresh()
    sub_page = driver.page_source
    sub_soup = BeautifulSoup(sub_page, "html.parser")

    for c, i in enumerate(sub_soup.find_all('div', {'id':'subCategoryContainer'} )):
        sub_cat = st.clear_extra_spaces(i.text)
        print(sub_cat)
        sub_url2 = store_url +ext+ i.find('a').attrs['href']
        driver.get(sub_url2)
        driver.refresh()

        if c == 0:

            try:
                driver.find_element_by_class_name('numberItemsPerPage').find_elements_by_tag_name('a')[1].click()
                driver.refresh()
                page_limit = 50
                print('50 items per page')
            except:
                page_limit = 10
                print('10 items per page')
                pass

        sub_page2 = driver.page_source
        sub_soup2 = BeautifulSoup(sub_page2, "html.parser")


        while sub_soup2.find('div', {'class':'itemListNavPagination'}):

            items_left = sub_soup2.find('div', {'class': 'numberOfShowingResults'}).text.split()

            for m, pic in zip(sub_soup2.find_all('td', {'name': re.compile(r'^itm_numlink')}), sub_soup2.find_all('td', {'name': re.compile(r'^itemthumbnail')}) ):

                num_link = m.attrs['name']
                print(num_link)
                try:
                    if driver.find_element_by_name(num_link):

                        #if pic.find('img').attrs['src'] == '/storefrontCommerce/imageContent.do?contentKey=noimage&size=THUMBNAIL':

                        sku = m.find('a').text
                        item_no = num_link.rsplit('k', 1)[1]
                        name = sub_soup2.find('td', {'name': 'itm_proddesc'+item_no}).text
                        print(item_no, sku, name)
                        product_df.at[sku, 'SKU #'] = sku
                        product_df.at[sku, 'Product Name'] = name
                        product_df.at[sku, 'Image'] = pic.find('img').attrs['src']#'/storefrontCommerce/imageContent.do?contentKey=noimage&size=THUMBNAIL'
                        product_df.at[sku, '48WS Category'] = sub_cat
                            #continue

                        # driver.find_element_by_name(num_link).click()
                        # driver.refresh()
                        #
                        # page3 = driver.page_source
                        # sub_soup3 = BeautifulSoup(page3, "html.parser")
                        # image = ''
                        # if sub_soup3.find('div', {'id':'itemDetailContainer'}):
                        #     image = sub_soup3.find('div', {'id':'itemDetailContainer'}).find('img').attrs['src']
                        #     image = store_url + ext + image
                        # #print(image)
                        # description = ''
                        # if sub_soup3.find('td', {'colspan':'15'}):
                        #     description = st.clear_extra_spaces(sub_soup3.find('td', {'colspan':'15'}).text)
                        #     #print(description)
                        # table = sub_soup3.find('table')
                        #
                        # item_li = [row.text for row in table.find_all('td')[:2]]
                        # print(item_li[1])
                        # sku = item_li[0]
                        # product_df.at[sku, 'SKU #'] = sku
                        # product_df.at[sku, 'Product Name'] = item_li[1]
                        # product_df.at[sku, 'Description'] = description
                        # product_df.at[sku, 'Image'] = image
                        # product_df.at[sku, '48WS Category'] = sub_cat
                        #
                        # driver.back()
                        # driver.refresh()
                except:
                    continue

                    #break


            if items_left[3] == items_left[5]:
                break

            if int(items_left[5]) - int(items_left[3]) <= page_limit:
                try:
                    driver.find_element_by_class_name('itemListNavPagination').find_elements_by_tag_name('a')[-1].click()
                except:
                    pass
            else:
                try:
                    driver.find_element_by_class_name('itemListNavPagination').find_elements_by_tag_name('a')[-2].click()
                except:
                    pass

            print('next page')

            driver.refresh()
            sub_page2 = driver.page_source
            sub_soup2 = BeautifulSoup(sub_page2, "html.parser")


        #break


    #break

st.export_df(product_df, company, same_company=True, url=store_url, version='products')
