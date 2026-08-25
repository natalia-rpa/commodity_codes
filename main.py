from sqlite3.dbapi2 import Row
import spreadsheet_handler
import sap_handler 
import app

import configparser

config = configparser.ConfigParser()
config.read('static/config.ini')

id_spreadsheet = config['GoogleSheets']['id_spreadsheet']
sap_task_sheet = config['GoogleSheets']['sap_task_sheet']
desc_task_sheet = config['GoogleSheets']['desc_task_sheet']
guide_sheet = config['GoogleSheets']['guide_sheet']
excel_path = config['LocalFiles']['excel_path']


def main_sap():

    df, sheet = spreadsheet_handler.connect_to_google_sheets(sap_task_sheet)

    # diff  Commodity_Code final HS CODE
    diff_df = df[df['Commodity_Code'] != df['final HS CODE']]

    # group by final HS CODE
    group_df = diff_df.groupby('final HS CODE')

    session = sap_handler.init_sap()

    print("connected to SAP\n")
    for hs_code, group_data in group_df:
        print("updating HS Code: ", hs_code)
        spreadsheet_handler.update_data_sheets(group_data, sheet)

        if not sap_handler.update_sap(session, group_data, hs_code):
            print("sap problem \n")
            break

    print("sap task complete\n")
    session.findById("wnd[0]/tbar[0]/btn[3]").press



import pandas as pd
import os
import spreadsheet_handler

def main_desc():

    guide_df, guide_sheet = spreadsheet_handler.connect_to_google_sheets(guide_sheet)

    input_codes = guide_df.iloc[:, 2].dropna().astype(str).str.strip().unique()

    excel_path = os.path.join("data", "Nomenclature EN.xlsx")

    nom_df = pd.read_excel(excel_path, dtype=str)
    
    # a = codes, g = descriptions of Nomenclature EN.xlsx
    col_a = nom_df.columns[0]
    col_g = nom_df.columns[6]

    # col c of guide sheet
    col_c = guide_df.iloc[:, 2]
    col_c = col_c.dropna()
    col_c = col_c.astype(str).str.strip()
    input_codes = col_c.unique()

    
    # strip spaces
    nom_df['search_code'] = nom_df[col_a].astype(str).str.replace(' ', '')

    # start searching
    results_list = []
    
    for code in input_codes:
            
        # remove last 2 characters
        prefix = code[:-2]
        
        # find matching codes with prefix
        matches = nom_df[nom_df['search_code'].str.startswith(prefix, na=False)]
        
        for _, match_row in matches.iterrows():
            results_list.append({
                'Original Input Code': code,
                'Matched Excel Code': match_row[col_a],
                'Description': match_row[col_g]
            })

    # convert to df
    results_df = pd.DataFrame(results_list)
    print(f"\nscraping complete. Found {len(results_df)} total matching variations.")

    _, desc_sheet = spreadsheet_handler.connect_to_google_sheets(desc_task_sheet)

    spreadsheet_handler.upload_to_desc_sheet(results_df, desc_sheet)

    

if __name__ == "__main__":
    ui = app.commodity_code_updater_app(main_sap_task=main_sap, main_desc_task=main_desc)
    ui.mainloop()




# def main_update_data():
    
#     df = web_handler.scrap(df)
#     now = datetime.now()
    
#     page.goto("https://circabc.europa.eu/ui/group/0e5f18c2-4b2f-42e9-aed4-dfe50ae1263b/library/566dd333-1deb-4235-982a-4fdeaf3657c1?p=1&n=-1&sort=name_ASC")
    
#     current_month_str = now.strftime("%m - %B") 
#     dynamic_pattern = re.compile(f"^{current_month_str}$")

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()

#         page.get_by_role("table").locator("a").filter(has_text=dynamic_pattern).click()

#         page.get_by_role("link", name="Nomenclature EN.xlsx").click()

#         with page.expect_download() as download3_info:
#             page.get_by_text("Download", exact=True).click()
#             download3 = download3_info.value
#             download3.save_as("Nomenclature EN.xlsx")



     
# import re
# from datetime import datetime
# from playwright.sync_api import sync_playwright
# import pandas as pd

# def main_download_data():
    
#     df = web_handler.scrap(df)
#     now = datetime.now()
    
#     page.goto("https://circabc.europa.eu/ui/group/0e5f18c2-4b2f-42e9-aed4-dfe50ae1263b/library/566dd333-1deb-4235-982a-4fdeaf3657c1?p=1&n=-1&sort=name_ASC")
    
#     current_month_str = now.strftime("%m - %B") 
#     dynamic_pattern = re.compile(f"^{current_month_str}$")

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()

#         page.get_by_role("table").locator("a").filter(has_text=dynamic_pattern).click()

#         page.get_by_role("link", name="Nomenclature EN.xlsx").click()

#         with page.expect_download() as download3_info:
#             page.get_by_text("Download", exact=True).click()
#             download3 = download3_info.value
#             download3.save_as("Nomenclature EN.xlsx")
