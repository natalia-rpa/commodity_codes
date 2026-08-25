import gspread
import pandas as pd


# input sheet name, return df and sheet
def connect_to_google_sheets(sheet_name):
    print("connect to Google Sheets\n")

    try:
        gc = gspread.service_account(filename='static/secrets/credentials.json')
        spreadsheet_url = "https://docs.google.com/spreadsheets/d/1-NTvWqIKwqjEkUMHVL6ubhx_x9TiPwqxsXD7kZSS3WU/edit"
        ss = gc.open_by_url(spreadsheet_url)
        sheet = ss.worksheet(sheet_name) 
        rows = sheet.get_all_values()

        headers = [h.strip() for h in rows[0]] # get headers
        df = pd.DataFrame(rows[1:], columns=headers)

        df['sheet_row'] = range(2, len(df) + 2)
        
    except Exception as e:
        print(f"Error connecting to Google Sheets ({sheet_name}): {e}\n")
        return 
    return df, sheet



def update_data_sheets(group_data, sheet):
    print("updating Google Sheets")
    cells_to_update = []
    commodity_col_index = 7

    hs_code = group_data['final HS CODE'].iloc[0]

    for _, row_data in group_data.iterrows():
        sheet_row = row_data['sheet_row']
        cells_to_update.append(gspread.Cell(row=sheet_row, col=commodity_col_index, value=group_data['final HS CODE'].iloc[0]))
    
    # push changes
    sheet.update_cells(cells_to_update, value_input_option='USER_ENTERED')
    print(f"sheets updated: {len(cells_to_update)} rows changed to {hs_code}\n")


def upload_to_desc_sheet(results_df, sheet):
    print("Uploading data to 'desc' sheet...")
    try:
        sheet.clear()

        # select code and description columns 
        upload_df = results_df[['Matched Excel Code', 'Description']].copy()
        
        # rename for desc sheet columns
        upload_df.columns = ['Code', 'Description']

        # convert to df to list
        data_to_upload = [upload_df.columns.values.tolist()] + upload_df.values.tolist()

        # push data
        sheet.update(range_name='A1', values=data_to_upload, value_input_option='USER_ENTERED')
        
        print(f"Successfully uploaded {len(upload_df)} rows to Google Sheets!")
        
    except Exception as e:
        print(f"Error uploading to 'desc' sheet: {e}")
        raise Exception(f"Failed to upload data to Google Sheets: {e}")