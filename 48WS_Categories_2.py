from selenium import webdriver
from bs4 import BeautifulSoup

import Scraping_Tools as st
import time
import pandas as pd




#trying to scrape categores from vault
# http://www.vault.48ws.com/login.aspx
url = 'http://www.vault.48ws.com/login.aspx'
email = 'evan@48ws.com'
password = 'evan2018'
#login_page = st.render_page(url)
category_url = 'http://www.vault.48ws.com/admin-categories.aspx'
category_df = pd.DataFrame(columns=['Category ID', 'Category', 'Sub Category', 'Sub Category 2'])

driver = webdriver.Chrome()
driver.get(url)
username = driver.find_element_by_id('ctl00_ContentPlaceHolder1_txtEmail')
username.send_keys(email)
pw = driver.find_element_by_id('ctl00_ContentPlaceHolder1_txtPassword')
pw.send_keys(password)
driver.find_element_by_name('ctl00$ContentPlaceHolder1$btnLogin').click()
driver.get(category_url)
ids = driver.find_elements_by_tag_name('li')


for li in ids:

    print(li.text)
    cat1 = li.text
    #print('test')
    for item in li.find_elements_by_tag_name('a'):

        if item.get_attribute('href'):
            print(item.get_attribute('href'))
            item_url = item.get_attribute('href')


            sub_driver = webdriver.Chrome()
            sub_driver.get(item_url)
            username = sub_driver.find_element_by_id('ctl00_ContentPlaceHolder1_txtEmail')
            username.send_keys(email)
            pw = sub_driver.find_element_by_id('ctl00_ContentPlaceHolder1_txtPassword')
            pw.send_keys(password)
            sub_driver.find_element_by_name('ctl00$ContentPlaceHolder1$btnLogin').click()
            #time.sleep(3)
            sub_driver.get(category_url)
            sub_driver.get(item_url)
            #time.sleep(3)

            page = sub_driver.page_source

            sub_soup = BeautifulSoup(page, "html.parser")


            if sub_soup.find('li', {'style':'list-style-image:url(~/img/darkicon.png); font-size:12px'}) is not None:
                print('sub items')
                sub_item_list = sub_soup.find_all('li',{'style':'list-style-image:url(~/img/darkicon.png); font-size:12px'})
                #print(sub_item_list)
                for a in sub_item_list:


                    name_href = [ b for b in a ]
                    print(name_href[0].attrs['name'])
                    print(name_href[1].text)
                    cat2 = name_href[1].text
                    cat2 = st.clean_punctuation(cat2)
                    cat2 = st.clear_extra_spaces(cat2)
                    item_id = name_href[0].attrs['name']

                    category_df.at[item_id, 'Category ID'] = item_id
                    category_df.at[item_id, 'Sub Category'] = cat2
                    print()

            sub_driver.close()

        elif item.get_attribute('name'):

            print(item.get_attribute('name'))
            item_id = item.get_attribute('name')

            cat1 = st.clean_punctuation(cat1)
            cat1 = st.clear_extra_spaces(cat1)

            category_df.at[item_id, 'Category ID'] = item_id
            category_df.at[item_id, 'Category'] = cat1
            print()


category_df.to_excel('categories_2.xlsx', index=False)


