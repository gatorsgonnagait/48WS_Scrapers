import pandas as pd
import os.path as path
import urllib.request


# too many instances that the scraper got, clean the duplicates

company_url = 'https://www.ingersollrandproducts.com'
company = 'Ingersoll_Rand'
file_path = company + path.sep
product_numbers = pd.read_excel(company+path.sep+company+'_fixed.xlsx')
fixed_df = pd.DataFrame()

item_set = set()

for i in product_numbers.index:
    name = product_numbers.at[i, 'Product Name']
    if not pd.isnull(product_numbers.at[i, 'Image']) and name not in item_set:

        item_set.add(name)
        fixed_df

