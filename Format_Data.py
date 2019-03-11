import pandas as pd
import numpy as np


if __name__ == '__main__':

    file = 'ingersoll2_rand'
    data_set = pd.read_csv(file+'.csv')
    fixed_data = pd.DataFrame(columns=['Product Name', 'Image', 'Manufacturer_URL', 'Weight', 'Manufacturer', 'Description', 'Quick Overview', 'Details', 'Group Name', 'Info/Size/Color', 'UPC'])
    sku_count = 0
    category = ''

    website_url = data_set['web-scraper-start-url'].iloc[0]

    website_url = website_url[:website_url.find('.com')+ 4]
    sku = ''
    for i in data_set.index:
        sku = data_set.at[i, 'sku']

        if pd.isnull(sku):
            sku = file[:-4]+'_'+str(sku_count)
            sku_count+=1
        print(sku)

        #fixed_data.at[sku, 'Category'] = category
        fixed_data.at[sku, 'Product Name'] = data_set.at[i, 'item_name']
        fixed_data.at[sku, 'Image'] = data_set.at[i, 'image-src']
        fixed_data.at[sku, 'Description'] = data_set.at[i, 'description']
        print(data_set.at[i, 'quick_overview'])
        fixed_data.at[sku, 'Quick Overview'] = data_set.at[i, 'quick_overview']
        fixed_data.at[sku, 'Manufacturer_URL'] = data_set.at[i, 'links-href']

        category = data_set.at[i, 'category_links']
        last_char_is_blank = False
        index = 0
        for i, s in enumerate(category):
            if s == ' ':
                if last_char_is_blank:
                    index = i-1
                    break
                else:
                    last_char_is_blank = True

        print(category[:index])
        fixed_data.at[sku, 'Group Name'] = category[:index]
        print()

    fixed_data.to_excel(file+'_fixed.xlsx')



