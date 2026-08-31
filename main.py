from sqlite3.dbapi2 import Row
import spreadsheet_handler
import sap_handler 
import app

import pandas as pd
import os
import configparser

import web_handler
from logger_setup import get_logger, log_phase

logger = get_logger(__name__)

config = configparser.ConfigParser()
config.read('static/config.ini')

id_spreadsheet = config['GoogleSheets']['id_spreadsheet']
sap_task_sheet = config['GoogleSheets']['sap_task_sheet']
desc_task_sheet = config['GoogleSheets']['desc_task_sheet']
guide_sheet = config['GoogleSheets']['guide_sheet']



def main_sap():

    log_phase(logger, "SAP TASK STARTED")
    logger.info("Goal: update commodity codes in SAP, then sync successful updates to Google Sheets.")

    log_phase(logger, "STEP 1 — Load SAP task sheet from Google Sheets")
    df, sheet = spreadsheet_handler.connect_to_google_sheets(sap_task_sheet)

    log_phase(logger, "STEP 2 — Find rows that need an update")

    # drop rows where column K = updated
    df = df[df['K'] != 'UPDATED']
    # diff  Commodity_Code final HS CODE
   # diff_df = df[df['Commodity_Code'] != df['final HS CODE']]
    logger.info(
        "Rows where Commodity_Code differs from final HS CODE: %d (out of %d total)",
        len(diff_df),
        len(df),
    )

    skipped = []

    #check if HS code have 8 digits — invalid rows go to skipped (no spreadsheet update)
    log_phase(logger, "STEP 3 — Validate final HS CODE (must be exactly 8 digits)")
    hs_lengths = diff_df['final HS CODE'].astype(str).str.len()
    invalid_df = diff_df[hs_lengths != 8]
    for _, row in invalid_df.iterrows():
        code = str(row['final HS CODE'])
        material = str(row.get('Material', ''))
        reason = f"final HS CODE must be 8 digits (got '{code}')"
        logger.warning("SKIPPED material %s — %s", material, reason)
        skipped.append({"hs_code": code, "material": material, "reason": reason})

    diff_df = diff_df[hs_lengths == 8]
    logger.info("Valid rows ready for SAP: %d", len(diff_df))
    logger.info("Skipped (invalid HS length): %d", len(invalid_df))

    if diff_df.empty:
        log_phase(logger, "SAP TASK FINISHED — nothing to send to SAP")
        logger.info("Total skipped: %d. Spreadsheet was not changed for skipped rows.", len(skipped))
        return skipped

    # group by final HS CODE
    group_df = diff_df.groupby('final HS CODE')
    logger.info("Will process %d unique final HS CODE value(s).", group_df.ngroups)

    log_phase(logger, "STEP 4 — Connect to SAP and open update transaction")
    session = sap_handler.init_sap()

    log_phase(logger, "STEP 5 — Update each HS code group in SAP")
    updated_groups = 0
    for hs_code, group_data in group_df:
        materials = group_data['Material'].astype(str).tolist()
        logger.info(
            "--- Processing final HS CODE %s (%d material(s): %s) ---",
            hs_code,
            len(group_data),
            ", ".join(materials[:10]) + ("..." if len(materials) > 10 else ""),
        )

        ok, reason = sap_handler.update_sap(session, group_data, hs_code)
        if not ok:
            logger.warning(
                "SKIPPED HS CODE %s — SAP did not update. Reason: %s. Spreadsheet left unchanged.",
                hs_code,
                reason,
            )
            skipped.append({"hs_code": hs_code, "material": "", "reason": reason})
            continue

        logger.info("Writing successful SAP update for %s back to Google Sheets...", hs_code)
        spreadsheet_handler.update_data_sheets(group_data, sheet)
        updated_groups += 1

    log_phase(logger, "SAP TASK FINISHED")
    logger.info("Successfully updated groups: %d", updated_groups)
    logger.info("Skipped items: %d", len(skipped))
    session.findById("wnd[0]/tbar[0]/btn[3]").press()
    return skipped



def main_desc():
    log_phase(logger, "DESCRIPTION SCRAPING TASK STARTED")
    logger.info("Goal: look up commodity-code descriptions on the EU TARIC website and save them to Google Sheets.")

    log_phase(logger, "STEP 1 — Load guide sheet (source list of codes)")
    # run web_handler.scrap(df)
    df, _ = spreadsheet_handler.connect_to_google_sheets(guide_sheet)
    # remove duplicate commodity codes
   
    unique_codes = df.iloc[:, 2].dropna().astype(str).str.strip().drop_duplicates().tolist()

    unique_codes = unique_codes[1:]
    logger.info("Unique commodity codes to scrape: %d", len(unique_codes))
  
    log_phase(logger, "STEP 2 — Prepare destination sheet (clear old results)")
    _, desc_sheet = spreadsheet_handler.connect_to_google_sheets(desc_task_sheet)
    desc_sheet.clear()
    logger.info("Destination sheet cleared and ready for new scrape results.")

    log_phase(logger, "STEP 3 — Scrape EU TARIC website for each code")
    skipped = web_handler.scrap(unique_codes, desc_sheet)

    log_phase(logger, "DESCRIPTION SCRAPING TASK FINISHED")
    if skipped:
        logger.info("Skipped %d code(s) that could not be scraped.", len(skipped))
    return skipped



if __name__ == "__main__":
    log_phase(logger, "APPLICATION START")
    logger.info("Opening the Commodity Code Updater window.")
    ui = app.commodity_code_updater_app(main_sap_task=main_sap, main_desc_task=main_desc)
    ui.mainloop()



