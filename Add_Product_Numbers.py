import pickle
import Scraping_Tools as st
import os.path as path
import pandas as pd

pickle_in = open("category_IDs.pickle","rb")
category_dict = pickle.load(pickle_in)
company = 'XL_Screw'

company = st.clean_punctuation(company)
company_products = pd.read_excel(company + path.sep + company + '_products.xlsx')
company_products = company_products.fillna('')


for i in company_products.index:

    cat = st.clean_everything(key=company_products.at[i, '48WS Category'])
    print(cat)
    company_products.at[i, 'Category'] = category_dict[cat]


company_products.to_excel(company + path.sep + company + '_products_with_categories.xlsx', index=False)

