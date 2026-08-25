# from playwright.sync_api import sync_playwright
# import pandas as pd

# def scrap(df):

#     print("start")

#     scraped_descriptions = []

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()

#         commodity_code = 84314980
        
#         page.goto("https://ec.europa.eu/taxation_customs/dds2/taric/taric_consultation.jsp?Lang=en")
#         # for index, row in df.iterrows():
    
#         #     commodity_code = str(row.iloc[2]).strip()
            
#         #     # skip if empty row
#         #     if not commodity_code :
#         #         continue

#         #     print("scraping :" ,commodity_code )

#         #     try:
#         #         page.goto("https://ec.europa.eu/taxation_customs/dds2/taric/taric_consultation.jsp?Lang=en")
                

#         #         page.locator("#taricCode").click()
#         #         page.locator("#taricCode").fill(commodity_code)
            
#         #         page.get_by_role("button", name="Retrieve Measures").click()
                
#         #         page.wait_for_load_state("networkidle")
                
#         #         description_element = page.locator("description_td").first

#         #         print("description_element :" , description_element)
#         #         if description_element.is_visible():
#         #             desc_text = description_element.inner_text().strip()
#         #         else:
#         #             desc_text = "Description not found on page"
                    
#         #         scraped_descriptions.append(desc_text)
                
#         #     except Exception as e:
#         #         print(f"Error scraping {commodity_code}: {e}")
#         #         scraped_descriptions.append("Error during scraping")

#         # context.close()
#         # browser.close()

#     df['Scraped_Description'] = scraped_descriptions
    
#     print("Scraping complete!")
#     return df


#     import playwright 
# import re
# from playwright.sync_api import Playwright, sync_playwright, expect


# # def scrap(df) -> None:
# #     browser = playwright.chromium.launch(headless=False)
# #     context = browser.new_context()
# #     page = context.new_page()
# #     page.goto("https://ec.europa.eu/taxation_customs/dds2/taric/taric_consultation.jsp?Lang=en")
# #     page.locator("#taricCode").press("Shift+Dead")
# #     page.locator("#taricCode").click()
# #     page.locator("#taricCode").fill("84312000")
# #     page.get_by_role("button", name="Retrieve Measures").click()
# #     page.get_by_role("searchbox", name="Search").click()
# #     page.get_by_role("searchbox", name="Search").press("Shift+Dead")
# #     page.get_by_role("searchbox", name="Search").fill("84314920")
# #     page.get_by_role("button", name="Search").click()
# #     page1 = context.new_page()
# #     page1.goto("https://ec.europa.eu/search/?query_source=TAXUD&QueryText=84314920")
# #     page1.close()
# #     page.goto("https://ec.europa.eu/taxation_customs/dds2/taric/taric_consultation.jsp?Lang=en&SimDate=20260824&Area=&MeasType=&StartPub=&EndPub=&MeasText=&GoodsText=&op=&Taric=84312000&AdditionalCode=&search_text=goods&textSearch=&LangDescr=en&OrderNum=&Regulation=&measStartDat=&measEndDat=&DatePicker=24-08-2026")
# #     page.get_by_role("searchbox", name="Search").click()
# #     page.get_by_role("searchbox", name="Search").click()
# #     page.locator("#taricCode").click()
# #     page.locator("#taricCode").fill("84314920")
# #     page.get_by_role("button", name="Retrieve Measures").click()
# #     page.locator("[id=\"8431492005-5\"]").get_by_text("- - - -").click()
# #     page.get_by_role("cell", name="Certain types of steel shoes, with or without rubber pads attached thereto, whether or not assembled in a track chain, with a maximum length of 3000 mm :", exact=True).click()
# #     page.get_by_role("cell", name="-  -  -  -   Certain types of").click()
# #     page.get_by_role("cell", name="-  -  -  -   Certain types of").click()
# #     page.get_by_role("cell", name="Certain types of steel shoes, with or without rubber pads attached thereto, whether or not assembled in a track chain, with a maximum length of 3000 mm :", exact=True).click()
# #     page.get_by_role("cell", name="Certain types of steel shoes, with or without rubber pads attached thereto, whether or not assembled in a track chain, with a maximum length of 3000 mm :", exact=True).click()
# #     expect(page.locator("[id=\"8431492005-5\"]")).to_contain_text("Certain types of steel shoes, with or without rubber pads attached thereto, whether or not assembled in a track chain, with a maximum length of 3000 mm :")

# #     # ---------------------
# #     context.close()
# #     browser.close()


