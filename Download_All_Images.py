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
#company = 'Ajax Springs'
#company = 'Stelfast'
#company = 'Pipe Hangers'
company = 'Inweld'

company = st.add_underscores(company)
directory = company+os.path.sep
product_df = pd.read_excel(directory+company+'_products_with_categories_2.xlsx')
#product_df = pd.read_excel(directory+company+'_products.xlsx')
img_dict = {}
last_img_name = ''
version = 'with_images'
images_have_same_name = False
forward_slash_pos = 1
alt_forward_slash_pos = 1


if not os.path.exists(directory+'images'):
    os.makedirs(directory+'images')

for i in product_df.index:

    #img = product_df.at[i, 'Manufacturer_URL']+  product_df.at[i, 'Image']
    img = product_df.at[i, 'Image']
    if not pd.isnull(img):
        if img not in img_dict:
            img_dict[img] = img
            print(img)
            #if images_have_same_name:

            #forward_slash_pos = alt_forward_slash_pos
            img_dict[img] = st.download_image(directory, img, forward_slash_pos)

        product_df.at[i, 'Image'] = img_dict[img]
    else:
        product_df.at[i, 'Image'] = company+'_logo.jpg'


st.export_df(product_df, company, url=None, version=version, same_company=False)