import gspread
import pandas as pd


def connect_to_google_sheets():
    print("connect to Google Sheets\n")

    try:
        gc = gspread.service_account(filename='static/secrets/credentials.json')
        spreadsheet_url = "https://docs.google.com/spreadsheets/d/1-NTvWqIKwqjEkUMHVL6ubhx_x9TiPwqxsXD7kZSS3WU/edit"
        ss = gc.open_by_url(spreadsheet_url)
        sheet = ss.worksheet("data2") 
        rows = sheet.get_all_values()

        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        headers = [h.strip() for h in rows[0]]
        df = pd.DataFrame(rows[1:], columns=headers)

        df['sheet_row'] = range(2, len(df) + 2)
        
        # clean df
        df['final HS CODE'] = df['final HS CODE'].astype(str).str.replace("'", "").str.strip()
        
        # diff  Commodity_Code final HS CODE
        diff_df = df[df['Commodity_Code'] != df['final HS CODE']]

        # group by final HS CODE
        group_df = diff_df.groupby('final HS CODE')



    except Exception as e:
        print("error connecting to Google Sheets\n")
        return 
    return group_df, sheet



def update_google_sheets(group_data, sheet):
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