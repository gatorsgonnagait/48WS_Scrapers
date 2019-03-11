import pandas as pd
import os.path as path
import Scraping_Tools as st
import pickle


def build_simple_dict(categories_df):
    key = ''
    cat_dict = {}
    #generic_categories = {}
    for i in categories_df.index:
        # if not pd.isnull(categories_df.at[i, 'Sub Category 2']):
        #     key = categories_df.at[i, 'Sub Category 2']
        if not pd.isnull(categories_df.at[i, 'Sub Category']):
            key = categories_df.at[i, 'Sub Category']
        elif not pd.isnull(categories_df.at[i, 'Category']):
            key = categories_df.at[i, 'Category']
            #generic_categories[key] = key

        if key not in cat_dict:
            key_short = ''
            key = st.clean_punctuation(key)
            key = st.clean_adjectives(key)
            key = st.clean_numbers(key)
            for w in key.split():
                w2 = st.clean_words(w)
                key_short += w2+' '
            key_short = st.unique_str(key_short)
            #cat_dict[key_short] = [0, key, False, '', categories_df.at[i, 'Category ID']]
            cat_dict[key_short] = categories_df.at[i, 'Category ID']
            # if key not in generic_categories and len(key.split()) == 1:
            #     generic_categories[key] = key

    return cat_dict


if __name__ == '__main__':

    categories_48ws = pd.read_excel('48ws_categories.xlsx')

    cat_dict = build_simple_dict(categories_48ws)

    pickle_out = open('category_IDs.pickle', 'wb')
    pickle.dump(cat_dict, pickle_out)
    pickle_out.close()
