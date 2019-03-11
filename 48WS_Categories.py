from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import re

site_url = 'http://www.48ws.com'
ext = '/categories/'
link = urllib.request.urlopen(site_url+ext)
soup = BeautifulSoup(link.read(), "html.parser")
category_df = pd.DataFrame()
c = 0
i = 0
#j = 0
parent_categories = soup.find_all('div', id=re.compile(r'^ctl00_dlCategories_ct'))
product_df = pd.DataFrame(columns=['Category ID','Category','Sub Category','Sub Category 2'])
for cat in parent_categories:
    parent = cat.find('a').text.strip()
    if parent[:2] == '> ':
        parent = parent[2:]
    print()
    print(parent)
    cat_id = cat.find('a').attrs['href'].replace(' ', '-')
    sub_url = site_url + cat_id
    sub_link = urllib.request.urlopen(sub_url)
    sub_soup = BeautifulSoup(sub_link.read(), "html.parser")

    for li in sub_soup.find_all('div', id=re.compile(r'^ctl00_ContentPlaceHolder1_dlCategories_ct')):

        if c%2 == 1:
            if li.find('a').attrs['href'][:3] != '/ct':
                break
            s2_url = site_url + li.find('a').attrs['href'].replace(' ', '-')
            print(s2_url)
            s2_link = urllib.request.urlopen(s2_url)
            s2_soup = BeautifulSoup(s2_link.read(), "html.parser")
            child = li.find('a').text.strip()

            category_df.at[i, 'Category ID'] = cat_id[3:8]
            category_df.at[i, 'Category'] = parent
            category_df.at[i, 'Sub Category'] = child
            print(child)

            # must go to one more sub category
            #temp_df = pd.DataFrame(columns=['Category ID','Category','Sub Category','Sub Category 2','Product'])
            i+=1
            if s2_soup.find_all('div', id=re.compile(r'^ctl00_ContentPlaceHolder1_dlCategories_ct')):
                print('one more level to go ')
                j = 0
                for prod in s2_soup.find_all('div', id=re.compile(r'^ctl00_ContentPlaceHolder1_dlCategories_ct')):

                    if j%2 == 1:
                        grand_child = prod.find('a').text.strip()
                        #series = pd.Series([s2_url[3:8], parent, child, grand_child], index=['Category ID','Category','Sub Category','Sub Category 2'])
                        category_df.at[i, 'Category ID'] = prod.find('a').attrs['href'][3:8]
                        category_df.at[i, 'Category'] = parent
                        category_df.at[i, 'Sub Category'] = child
                        category_df.at[i, 'Sub Category 2'] = grand_child
                        print(grand_child)
                        i+=1
                        #category_df.append(series, ignore_index=True)
                    j+=1

        c+=1

    #break
#stat_series = pd.Series([schedule.at[i, 'Game'], schedule.at[i, 'spread'], schedule.at[i, 'expected_difference'], schedule.at[i, 'result']], index=['Game', 'spread', 'expected difference', 'result'])
category_df.to_excel('48ws_categories.xlsx', index=False)