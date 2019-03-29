import pandas as pd
import Scraping_Tools as st
import os




img_dict = {}
last_img_name = ''
version = 'with_images'
company = input('Enter Company Name: ')
company = st.add_underscores(company)
directory = company+os.path.sep
product_df = pd.read_excel(directory+company+'_products_with_categories.xlsx')
forward_slash_pos = int(input('How many slashes from the right is image file in the url? Its usually 1. '))


try:

    if not os.path.exists(directory+'images'):
        os.makedirs(directory+'images')

    for i in product_df.index:

        img = product_df.at[i, 'Image']
        if not pd.isnull(img):
            if img not in img_dict:
                img_dict[img] = img
                print(img)

                img_dict[img] = st.download_image(directory, img, forward_slash_pos)

            product_df.at[i, 'Image'] = img_dict[img]
        else:
            product_df.at[i, 'Image'] = company+'_logo.jpg'


    st.export_df(product_df, company, url=None, version=version, same_company=False)
except:
    os._exit(1)