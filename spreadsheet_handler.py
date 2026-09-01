import gspread
import pandas as pd
from logger_setup import get_logger
import configparser
logger = get_logger(__name__)

#from config.ini get spreadsheet url
config = configparser.ConfigParser()
config.read('static/config.ini')
id_spreadsheet = config['GoogleSheets']['id_spreadsheet']

# input sheet name, return df and sheet
def connect_to_google_sheets(sheet_name):
    logger.info("Opening Google Sheet tab: '%s'...", sheet_name)

    try:
        gc = gspread.service_account(filename='static/secrets/credentials.json')
        spreadsheet_url = "https://docs.google.com/spreadsheets/d/" + id_spreadsheet + "/edit"
        ss = gc.open_by_url(spreadsheet_url)
        sheet = ss.worksheet(sheet_name) 
        rows = sheet.get_all_values()

        headers = [h.strip() for h in rows[0]] # get headers
        df = pd.DataFrame(rows[1:], columns=headers)

        df['sheet_row'] = range(2, len(df) + 2)
        logger.info("Loaded '%s': %d data row(s).", sheet_name, len(df))
        
    except Exception as e:
        logger.error(
            "Failed to open Google Sheet tab '%s'. Check credentials and sheet name. Details: %s",
            sheet_name,
            e,
            exc_info=True,
        )
        return 
    return df, sheet



def update_data_sheets(group_data, sheet):
    cells_to_update = []
    update_col_index = 11
   # hs_code = group_data['final HS CODE'].iloc[0]

    for _, row_data in group_data.iterrows():
        sheet_row = row_data['sheet_row']
        cells_to_update.append(gspread.Cell(row=sheet_row, col=update_col_index, value="UPDATED"))
    
    # push changes
    sheet.update_cells(cells_to_update, value_input_option='USER_ENTERED')
    logger.info(
        "Google Sheets updated: set %d rows.",
       # hs_code,
        len(cells_to_update),
    )


def upload_to_desc_sheet(results_df, sheet):
    try:
        
        upload_df = results_df[['Searched_Code', 'Section', 'Section_Description', 'Chapter', 'Chapter_Description', 'Code', 'Description']].fillna("").copy()
        
        data_to_upload = [upload_df.columns.values.tolist()] + upload_df.values.tolist()
        
        sheet.update(range_name='A1', values=data_to_upload, value_input_option='USER_ENTERED')
        logger.info("Saved scrape results to Google Sheets: %d row(s) written.", len(upload_df))
        
    except Exception as e:
        logger.error("Failed to upload scrape results to Google Sheets: %s", e, exc_info=True)
        raise Exception(f"Failed to upload data to Google Sheets: {e}")
