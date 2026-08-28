from playwright.sync_api import sync_playwright
import pandas as pd
import time
import re
from playwright.sync_api import Playwright, sync_playwright, expect, TimeoutError as PlaywrightTimeoutError
import spreadsheet_handler
from logger_setup import get_logger

logger = get_logger(__name__)

INVALID_CODE_REASON = "Invalid format for the goods nomenclature code"

def scrap(codes_list,sheet):

    total = len(codes_list)
    logger.info("Starting website scrape for %d commodity code(s).", total)
   
 
    scraped_results = []
    skipped = []
    ok_count = 0
    fail_count = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        logger.info("Browser started (headless).")
        
        #commodity_code = "84314980"
        
        for index, commodity_code in enumerate(codes_list, start=1):

            if not commodity_code or commodity_code.lower() == "nan":
                logger.warning("Code %d/%d skipped — empty or invalid value: %r", index, total, commodity_code)
                continue

            logger.info("Code %d/%d — looking up %s on TARIC...", index, total, commodity_code)

            try:
                page.goto("https://ec.europa.eu/taxation_customs/dds2/taric/taric_consultation.jsp?Lang=en")
                #time.sleep(2)
                page.wait_for_selector("#taricCode", state="visible")
                page.locator("#taricCode").fill(commodity_code)
                #time.sleep(2)
            
                page.get_by_role("button", name="Retrieve Measures").click()
                #time.sleep(2)
                page.wait_for_load_state("networkidle")

                page.locator("#div_description").wait_for(state="visible", timeout=10000)
                #time.sleep(2)

                # extract chapter and section description
                section_locator = page.locator("td.chaplabel").filter(has_text=re.compile(r"SECTION", re.IGNORECASE))
                section_text = section_locator.first.inner_text().strip() if section_locator.count() > 0 else ""
            
                section_desc_locator = section_locator.locator("..").locator(".tddescription")
                section_desc_text = section_desc_locator.inner_text().strip() if section_desc_locator.count() > 0 else ""
                section_desc_text = re.sub(r'\s+', ' ', section_desc_text)
                # print("section_desc_text :" , section_desc_text)
                chapter_locator = page.locator("td.chaplabel").filter(has_text=re.compile(r"CHAPTER", re.IGNORECASE))
                chapter_text = chapter_locator.first.inner_text().strip() if chapter_locator.count() > 0 else ""
                
                chapter_desc_locator = chapter_locator.locator("..").locator(".tddescription")
                chapter_desc_text = chapter_desc_locator.inner_text().strip() if chapter_desc_locator.count() > 0 else ""
                chapter_desc_text = re.sub(r'\s+', ' ', chapter_desc_text)


            # print("chapter_desc_text :" , chapter_desc_text)

            # main data extraction
            #nomenclature code extraction = each commmodity code
                rows = page.locator("#div_description div[class*='nomenclaturecode codelev']").all()
            
                #time.sleep(2)
                # clean scraped_results list
                

                for row in rows:
                    # Get the level class  'nomenclaturecode codelev6 evenLine'
                    class_attr = row.get_attribute("class") or ""
                    level_match = re.search(r'codelev(\d+)', class_attr)
                    level = level_match.group(1) if level_match else ""

                    if not level:
                            continue


                    # Get Code from tdlabel
                    tdlabel = row.locator(".tdlabel")
                    code_text = tdlabel.inner_text().strip() if tdlabel.count() > 0 else ""
                    code_text = re.sub(r'\s+', ' ', code_text) #clean

                    # Get desc from tddescription -> to_highlight
                    tddesc = row.locator(".tddescription .to_highlight")
                    if tddesc.count() == 0:
                        tddesc = row.locator(".tddescription") # Fallback if to_highlight isn't present
                    desc_text = tddesc.inner_text().strip() if tddesc.count() > 0 else ""
                    desc_text = re.sub(r'\s+', ' ', desc_text)
                    #print("desc_text :" , desc_text)

                    # skip if description = 'Other' or `Other :`
                    if desc_text == 'Other' or desc_text == 'Other :':
                        continue

                    scraped_results.append({
                                "Searched_Code": commodity_code,
                                "Section": section_text,
                                "Section_Description": section_desc_text,
                                "Chapter": chapter_text,
                                "Chapter_Description": chapter_desc_text,
                                "Level": level,
                                "Code": code_text,
                                "Description": desc_text
                            })
                
              
                logger.info(
                    "Code %d/%d — OK: found %d description line(s) for %s. Saving to Google Sheets...",
                    index,
                    total,
                    len(rows),
                    commodity_code,
                )
              
                results_df = pd.DataFrame(scraped_results)  
                spreadsheet_handler.upload_to_desc_sheet(results_df, sheet)
                ok_count += 1
            except PlaywrightTimeoutError:
                fail_count += 1
                logger.warning(
                    "Code %d/%d — SKIPPED %s — %s",
                    index,
                    total,
                    commodity_code,
                    INVALID_CODE_REASON,
                )
                skipped.append({
                    "hs_code": commodity_code,
                    "material": "",
                    "reason": INVALID_CODE_REASON,
                })
            except Exception as e:
                fail_count += 1
                logger.error(
                    "Code %d/%d — FAILED for %s: %s",
                    index,
                    total,
                    commodity_code,
                    e,
                    exc_info=True,
                )
                skipped.append({
                    "hs_code": commodity_code,
                    "material": "",
                    "reason": str(e),
                })

        context.close()
        browser.close()

    logger.info(
        "Scraping finished. Success: %d | Failed/skipped: %d | Total attempted: %d",
        ok_count,
        fail_count,
        total,
    )
    return skipped
