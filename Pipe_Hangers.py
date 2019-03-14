import Scraping_Tools as st
from bs4 import BeautifulSoup
import re
from selenium import webdriver

#url = 'http://www.pipehangers.com/'
#store_url = 'https://storefront.pipehangers.com/storefrontCommerce/categorybrowse.do?category-name=Pipe+Attachments&path=&currentPage=1&numResults=10&expanded=
ext = '/storefrontCommerce/'
store_url = 'https://storefront.pipehangers.com'
prod_ext = 'products.html'
manufacturer = 'Pipe Hangers'
driver = webdriver.Chrome()
#driver.get(url)


company = st.add_underscores(manufacturer)
product_df = st.create_product_df()

driver.get(store_url)
            #time.sleep(3)



page = driver.page_source

soup = BeautifulSoup(page, "html.parser")

current_cat_no = 0

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

        if k == 0 and c == 0:
            driver.find_element_by_class_name('numberItemsPerPage').find_elements_by_tag_name('a')[1].click()
            print('50 items per page')


        sub_page2 = driver.page_source
        sub_soup2 = BeautifulSoup(sub_page2, "html.parser")


        while sub_soup2.find('div', {'class':'itemListNavPagination'}):

            items_left = sub_soup2.find('div', {'class': 'numberOfShowingResults'}).text.split()
            #print(items_left[3], items_left[5])

            #
            for m, pic in zip(sub_soup2.find_all('td', {'name': re.compile(r'^itm_numlink')}), sub_soup2.find_all('td', {'name': re.compile(r'^itemthumbnail')}) ):

                num_link = m.attrs['name']
                print(num_link)
                try:
                    if driver.find_element_by_name(num_link):

                        if pic.find('img').attrs['src'] == '/storefrontCommerce/imageContent.do?contentKey=noimage&size=THUMBNAIL':
                            print('no image, break')
                            sku = m.find('a').text
                            print(sku)
                            item_no = num_link.rsplit('k', 1)[1]
                            print(item_no)
                            name = sub_soup2.find('td', {'name': 'itm_proddesc'+item_no}).text
                            print(name)
                            product_df.at[sku, 'SKU #'] = sku
                            product_df.at[sku, 'Product Name'] = name
                            product_df.at[sku, 'Image'] = '/storefrontCommerce/imageContent.do?contentKey=noimage&size=THUMBNAIL'
                            product_df.at[sku, '48WS Category'] = sub_cat
                            #breakpoint()
                            continue

                        driver.find_element_by_name(num_link).click()
                        driver.refresh()

                        page3 = driver.page_source
                        sub_soup3 = BeautifulSoup(page3, "html.parser")
                        image = ''
                        if sub_soup3.find('div', {'id':'itemDetailContainer'}):
                            image = sub_soup3.find('div', {'id':'itemDetailContainer'}).find('img').attrs['src']
                            image = store_url + ext + image
                        #print(image)
                        description = ''
                        if sub_soup3.find('td', {'colspan':'15'}):
                            description = st.clear_extra_spaces(sub_soup3.find('td', {'colspan':'15'}).text)
                            #print(description)
                        table = sub_soup3.find('table')

                        item_li = [row.text for row in table.find_all('td')[:2]]
                        print(item_li[1])
                        sku = item_li[0]
                        product_df.at[sku, 'SKU #'] = sku
                        product_df.at[sku, 'Product Name'] = item_li[1]
                        product_df.at[sku, 'Description'] = description
                        product_df.at[sku, 'Image'] = image
                        product_df.at[sku, '48WS Category'] = sub_cat

                        driver.back()
                        driver.refresh()
                except:
                    pass

                    #break


            if items_left[3] == items_left[5]:
                break

            try:
                if int(items_left[5]) - int(items_left[3]) <= 50:
                    driver.find_element_by_class_name('itemListNavPagination').find_elements_by_tag_name('a')[-1].click()
                else:
                    driver.find_element_by_class_name('itemListNavPagination').find_elements_by_tag_name('a')[-2].click()
            except:
                break

            print('next page')

            #driver.refresh()
            sub_page2 = driver.page_source
            sub_soup2 = BeautifulSoup(sub_page2, "html.parser")


        #break


    #break

st.export_df(product_df, company, same_company=True, url=store_url, version='products')
