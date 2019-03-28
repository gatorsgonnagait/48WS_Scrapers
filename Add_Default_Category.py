import Scraping_Tools as st
import pandas as pd
import os as path
import Categorize_Products as cp

company = 'Inweld'
company = st.add_underscores(company)
company = st.clean_punctuation(company)
categories_48ws = pd.read_excel('48ws_categories.xlsx')
company_products = pd.read_excel(company + path.sep + company + '_products_with_categories.xlsx')
company_products = company_products.fillna('')
default_category = 'Gas Welding Equipment'
default_category = cp.clean_string(default_category)

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

cat_dict, gc = cp.build_categories_dic(categories_48ws)
gc_2 =  {**gc, **generic_categories}
gc_2 = cp.clean_dictionary(gc_2)

print(cat_dict[default_category])

for i in company_products.index:
    if not company_products.at[i, 'Category']:
        company_products.at[i, 'Category'] = str(cat_dict[default_category][4])


company_products.to_excel(company + path.sep + company + '_products_with_categories_2.xlsx', index=False)