import pandas as pd
import Scraping_Tools as st
import os
import numpy as np

#company = 'US Wire and Cable'
#company = 'XL Screw'
#company = 'PhD Manufacturing'
#company = 'Mule Head'
#company = 'Ingersoll Rand'
#company = 'All Material Handling'
company = 'Ajax Springs'

company = st.add_underscores(company)
directory = company+os.path.sep
product_df = pd.read_excel(directory+company+'_products_with_categories.xlsx')
#product_df = pd.read_excel(directory+company+'_products.xlsx')
img_set = set()
last_img_name = ''
version = 'with_categories_images'
images_have_same_name = False
forward_slash_pos = 1
alt_forward_slash_pos = 4


if not os.path.exists(directory+'images'):
    os.makedirs(directory+'images')

for i in product_df.index:

    img = product_df.at[i, 'Image']

    if img not in img_set and not pd.isnull(img):
        img_set.add(img)
        print(img)
        if images_have_same_name:
            forward_slash_pos = alt_forward_slash_pos
        last_img_name = st.download_image(directory, img, forward_slash_pos)
    product_df.at[i, 'Image'] = last_img_name


st.export_df(product_df, company, url=None, version=version, same_company=False)