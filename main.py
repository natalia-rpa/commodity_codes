from sqlite3.dbapi2 import Row
import spreadsheet_handler
import sap_handler 
import app
import web_handler

def main_sap():
    sheet_name = "data2"
    df, sheet = spreadsheet_handler.connect_to_google_sheets(sheet_name)
    index_to_update = 7
    
    # diff  Commodity_Code final HS CODE
    diff_df = df[df['Commodity_Code'] != df['final HS CODE']]

    # group by final HS CODE
    group_df = diff_df.groupby('final HS CODE')

    session = sap_handler.init_sap()

    print("connected to SAP\n")
    for _, group_data in group_df:
        if not sap_handler.update_sap(session, group_data):
            print("sap error\n")
            return
        spreadsheet_handler.update_google_sheets(group_data, sheet)


def main_desc():
    sheet_name = "guide"
    index_to_update = 7

    df, sheet = spreadsheet_handler.connect_to_google_sheets(sheet_name)

    df = web_handler.scrap(df)


    for row in df:
        if not web_handler.scrap(row):
            print("web error\n")
            return
        spreadsheet_handler.update_google_sheets2(row, sheet)
   

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
