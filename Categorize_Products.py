import pandas as pd
import os.path as path
import Scraping_Tools as st





def build_categories_dic(categories_df):
    key = ''
    cat_dict = {}
    generic_categories = {}
    for i in categories_df.index:
        if not pd.isnull(categories_df.at[i, 'Sub Category']):
            key = categories_df.at[i, 'Sub Category']
        elif not pd.isnull(categories_df.at[i, 'Category']):
            key = categories_df.at[i, 'Category']
            generic_categories[key] = key


        if key not in cat_dict:
            key_short = ''
            key = st.clean_punctuation(key)
            key = st.clean_adjectives(key)
            key = st.clean_numbers(key)
            for w in key.split():
                w2 = st.clean_words(w)
                key_short += w2+' '

            key_short = st.unique_str(key_short)
            cat_dict[key_short] = [0, key, False, '', categories_df.at[i, 'Category ID']]

            if key not in generic_categories and len(key.split()) == 1:
                generic_categories[key] = key

    return cat_dict, generic_categories


def clean_dictionary(dict):
    gc_2 = {}
    for k, v in dict.items():
        value_str = st.clean_adjectives(v)
        value_str = st.clean_punctuation(value_str)
        value_str = st.clean_numbers(value_str)
        k2 = ''
        v2 = ''

        for word in k.split():
            k2 += st.clean_words(word)+' '
        k2 = k2[:-1]

        for word in value_str.split():
            v2 += st.clean_words(word)+' '
        gc_2[k2] = v2[:-1]

    return gc_2

def clean_string(str):

    k2 = ''
    for word in str.split():
        k2 += st.clean_words(word) + ' '

    return k2[:-1]

def pick_most_relevant_category(item_line, cat_dict, generic_categories):
    generic_key = ''
    for w in item_line.split():
        word = st.clean_words(w)
        index = 0
        for key in cat_dict:
            if word in key.split():
                cat_dict[key][0] += 1
                starting_index = index
                for i, k in enumerate(key.split()[starting_index:]):
                    if word == k:
                        index = i
                        if cat_dict[key][2]:
                            cat_dict[key][0] += 1
                        else:
                            cat_dict[key][2] = True
                    else:
                        cat_dict[key][2] = False
            else:
                cat_dict[key][2] = False

        if word in generic_categories:
            generic_key = generic_categories[word].lower()
            cat_dict[generic_key][0] += 1.5
            cat_dict[generic_key][3] = generic_categories[word]

    maximum = max(cat_dict, key=cat_dict.get)
    max_value = max(cat_dict.values())
    return maximum, max_value, generic_key


def categorize_items(company_products, cat_dict, generic_categories, pre_categorized):

    done_already = {}
    for p in company_products.index:

        for k in cat_dict:
            cat_dict[k][0] = 0
            cat_dict[k][2] = False
            cat_dict[k][3] = ''

        if pre_categorized:
            name = company_products.at[p, '48WS Category']
            item_line = st.clean_punctuation(company_products.at[p, '48WS Category'])
        else:
            name = company_products.at[p, 'Product Name']
            item_line = st.clean_punctuation(company_products.at[p, 'Product Name'])

        item_line = st.clean_adjectives(item_line.lower())
        item_line = st.clean_numbers(item_line)

        if item_line in done_already:
            if done_already[item_line][2]:
                company_products.at[p, '48WS Category'] = done_already[item_line][0]
                company_products.at[p, 'Category'] = done_already[item_line][1]
            continue

        maximum, max_value, generic_key = pick_most_relevant_category(item_line, cat_dict, generic_categories)


        if max_value[0] == 2.5 and generic_key: # if no other categories have more than 1 count and the  generic key isnt null
            company_products.at[p, '48WS Category'] = cat_dict[generic_key][1]
            company_products.at[p, 'Category'] = str(cat_dict[generic_key][4])
            done_already[item_line] = [company_products.at[p, '48WS Category'], company_products.at[p, 'Category'], True]
        elif max_value[0] > 1:
            company_products.at[p, '48WS Category'] = cat_dict[maximum][1]
            company_products.at[p, 'Category'] = str(cat_dict[maximum][4])
            done_already[item_line] = [company_products.at[p, '48WS Category'], company_products.at[p, 'Category'], True]

        elif pre_categorized:

            item_line = st.clean_punctuation(company_products.at[p, 'Product Name'])
            item_line = st.clean_adjectives(item_line.lower())
            item_line = st.clean_numbers(item_line)

            if item_line in done_already:
                if done_already[item_line][2]:
                    company_products.at[p, '48WS Category'] = done_already[item_line][0]
                    company_products.at[p, 'Category'] = done_already[item_line][1]
                continue

            maximum, max_value, generic_key = pick_most_relevant_category(item_line, cat_dict, generic_categories)

            if max_value[0] == 2.5 and generic_key:
                company_products.at[p, '48WS Category'] = cat_dict[generic_key][1]
                company_products.at[p, 'Category'] = str(cat_dict[generic_key][4])
                done_already[item_line] = [company_products.at[p, '48WS Category'], company_products.at[p, 'Category'], True]
            elif max_value[0] > 1:
                company_products.at[p, '48WS Category'] = cat_dict[maximum][1]
                company_products.at[p, 'Category'] = str(cat_dict[maximum][4])
                done_already[item_line] = [company_products.at[p, '48WS Category'], company_products.at[p, 'Category'],True]
            else:
                done_already[item_line] = ['', '', False]

        else:
            done_already[item_line] = ['', '',False]

        print(name)
        print(max_value)
        print()

    return company_products


if __name__ == '__main__':

    #company = 'Ingersoll_Rand'
    #company = 'All_Material_Handling'
    #company = 'XL_Screw'
    #company = 'PhD_Manufacturing'
    #company = 'US_Wire_and_Cable'
    #company = 'Ajax Springs'
    #company = 'Pipe Hangers'
    #company = 'Inweld'
    company = 'Pipe Tytes'
    company = st.add_underscores(company)
    company = st.clean_punctuation(company)

    company_products = pd.read_excel(company + path.sep + company+'_products.xlsx')
    company_products = company_products.fillna('')
    categories_48ws = pd.read_excel('48ws_categories.xlsx')


    generic_categories = {'wrench': 'Combination Wrench', 'screwdriver': 'Screwdriver', 'saw': 'Saw Blade', 'grinder':'Grinders & Accessori', 'trolley': 'Trolley',
                          'drill':'Drill', 'scaler': 'Needle Scaler', 'nibbler': 'Nibblers & Shear', 'sander':'Orbit and Disc Sander', 'chain': 'Chain', 'clamp': 'Clamp',
                          'polisher': 'Polishers and Buffer', 'buffer':'Polishers and Buffer', 'engrave': 'Engraver', 'remover':'Polishers and Buffer',
                          'gasket': 'Engine Oil Drain Plug', 'fitting':'Fitting', 'hose':'Hose', 'lug':'Weld Lug', 'fuel': 'Fuel Transfer Pump Accessori',
                          'helmet':'Hard Hat', 'cable':'Cable Connector', 'adhesive':'Adhesiv', 'bayonet':'Conduit Connector', 'ferrule': 'Wire Ferrules & Bushing',
                          'electrode': 'Stick Electrode', 'gouging': 'Stick Electrode', 'torch':'Butane Torches','acetylene':'Butane Torches',
                          'cylinder':'Portable Air Tank', 'weld':'Gas Welding Equipment', 'regulator': 'air regulator','silver':'Industrial Raw Materials',
                          'copper':'copper', 'steel':'Alloy Steel', 'Aluminum':'Aluminum', 'Brass':'Brass', 'Bronze':'Bronze', 'Carbon':'Carbon Steel',
                          'Ceramic':'Ceramic', 'iron':'Cast Iron', 'Cork':'Cork', 'felt':'felt', 'fiberglass':'fiberglass','foam':'foam', 'plastics':'plastics',
                          'rubber':'rubber', 'tin':'tin','vinyl':'vinyl','stainless':'stainless steel','wire cloth':'wire cloth','conduit':'conduit connector',
                          'pipe':'plumbing pipe & tubing', 'cup':'welding nozzles', 'flux':'soldering flux', 'mig':'Gas Welding Equipment',
                          'tig': 'Gas Welding Equipment', 'collet':'collets', 'broco':'Gas Welding Equipment', 'metal':'Alloy Steel', 'dinse':'connector',
                          'connector':'connector', 'cap':'cap', 'handles':'welding torch handles', 'cutting':'Cutting Attachments', 'polycarbonate':'carbon steel',
                          'valve':'valves', 'caps':'caps', 'alloy':'Industrial Raw Materials', 'plug':'plug', 'adaptor':'adapters', 'adapter':'adapters',
                          'liner':'form liner', 'dura':'Welding Protection', 'fasteners':'fasteners anchors', 'anchors':'anchors', 'bolt':'bolt', 'lockwashers':'washer',
                          'cord':'cordage', 'imsul':'insulation', 'mount':'mounting base', 'restrain':'fitting restraints', 'firestop':'firestop accessories',
                          'channel':'strut channel', 'clevis': 'clevis fittings', 'seal':'sealer', 'roof':'roofing and siding'}

    cat_dict, gc = build_categories_dic(categories_48ws)
    gc_2 =  {**gc, **generic_categories}
    gc_2 = clean_dictionary(gc_2)

    company_products = categorize_items(company_products, cat_dict, gc_2, pre_categorized=True)
    #
    company_products.to_excel(company + path.sep + company + '_products_with_categorie.xlsx', index=False)