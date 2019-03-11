import pandas as pd
import os.path as path
import requests
from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup
import urllib.request
import os

def download_image(directory, img_url, forward_slash_pos):
    if img_url:
        file_name = img_url.rsplit('/', forward_slash_pos)[1] #split once from right by forward slash, then take 2nd item in list, which is everything after /
        ext = file_name.rsplit('.', 1)[1]
        file_name = file_name.rsplit('.', 1)[0]

        if ext =='.gif':
            ext = ".jpg"
        print(file_name+'.'+ext)
        file_name+='.'+ext
        #file_name = clean_punctuation(file_name)+'.'+ext
        picture_request = requests.get(img_url)
        if picture_request.status_code == 200:

            with open(directory+'images'+ path.sep+file_name, 'wb') as f:
                f.write(picture_request.content)
        return file_name


def clean_punctuation(str):
    clean = str.replace('"', '')
    clean = clean.replace('.', '')
    clean = clean.replace('\\', '')
    clean = clean.replace('/', ' ')
    clean = clean.replace('*', '')
    clean = clean.replace('|', '')
    clean = clean.replace(':', '')
    clean = clean.replace('<', '')
    clean = clean.replace('>', '')
    clean = clean.replace('?', '')
    clean = clean.replace('-', ' ')
    clean = clean.replace('&', '')
    clean = clean.replace(',', '')
    clean = clean.replace('(0)', '')
    clean = clean.replace('(10)', '')

    return clean

def clean_numbers(str):
    copy = str
    for s in str.split():
        if s.isdigit():
           copy = copy.replace(s, '')
    return copy

def clean_adjectives(str):
    clean = str.replace('super', '')
    clean = clean.replace('heavy', '')
    clean = clean.replace('pro', '')
    clean = clean.replace('high', '')
    clean = clean.replace(' and ', ' ')
    clean = clean.replace('series', '')
    clean = clean.replace('ultra', '')
    clean = clean.replace('type', '')
    clean = clean.replace('mini', '')
    clean = clean.replace('non', '')
    clean = clean.replace('impact', '')
    clean = clean.replace('combo', '')
    clean = clean.replace('kit', '')
    clean = clean.replace('angle', '')
    clean = clean.replace('general', '')
    clean = clean.replace('purpose', '')
    clean = clean.replace(' for ', ' ')
    clean = clean.replace('with', '')
    clean = clean.replace('built', '')
    clean = clean.replace('hi', '')
    clean = clean.replace(' in ', ' ')
    clean = clean.replace(' or ', ' ')
    clean = clean.replace('self', '')

    return clean

def clean_words(word):
    w = word.lower()
    if  w[-1] == 'v' :
        if len(w) == 1:
            w = 'cordless'
        elif w[-2].isdigit():
            w = 'cordless'
    elif w[:4] == 'weld':
        w = 'weld'
    elif w == 'gasoline' or w == 'gas':
        w = 'gas'
    elif w[-2:] == 'es':
        w = w[:-2]
    elif w[-1] == 's' or w[-1] == 'e':
        w = w[:-1]
    elif w[-3:] == 'ing':
        w = w[:-3]
    return w


def unique_str(str):
    return ' '.join(unique_list(str.split()))


def clean_everything(key):
    key_short = ''
    key = clean_punctuation(key)
    key = clean_adjectives(key)
    key = clean_numbers(key)
    for w in key.split():
        w2 = clean_words(w)
        key_short += w2 + ' '
    return unique_str(key_short)

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist


def render_page(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    r = driver.page_source
    return r


def create_product_df():
    product_df = pd.DataFrame(columns=['48WS.com URL', 'Category', 'SKU #', 'Product Name', 'Image', 'Manufacturer_URL', 'Weight','Manufacturer',
                                       'Description', 'Quick Overview', 'Details', 'Group Name', 'Info/Size/Color', 'UPC'])
    product_df.index.name = 'sku'
    return product_df

def clear_extra_spaces(str):
    str2 = str.lstrip()
    str2 = str2.rstrip()
    return re.sub(' +', ' ', str2)

def add_underscores(str):
    return str.replace(' ', '_')

def export_df(df, company, url, same_company, version):
    if not os.path.exists(company):
        os.makedirs(company)
    if url:
        df['Manufacturer_URL'] = url
    if same_company:
        df['Manufacturer'] = company
    df.to_excel(company + path.sep + company + '_'+version+'.xlsx', index=False)

def create_bs4_soup(url):
    link = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
    html = urllib.request.urlopen(link)
    return BeautifulSoup(html.read(), "html.parser")
