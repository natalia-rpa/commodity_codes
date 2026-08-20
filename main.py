import ssl
import win32com.client
import pandas as pd
import gspread



def connect_to_google_sheets():
    print("connect to Google Sheets\n")

    try:
        gc = gspread.service_account(filename='credentials.json')
        spreadsheet_url = "https://docs.google.com/spreadsheets/d/1-NTvWqIKwqjEkUMHVL6ubhx_x9TiPwqxsXD7kZSS3WU/edit"
        ss = gc.open_by_url(spreadsheet_url)
        sheet = ss.worksheet("data") 
        rows = sheet.get_all_values()

        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        headers = [h.strip() for h in rows[0]]
        df = pd.DataFrame(rows[1:], columns=headers)

        print(df.columns)

    except Exception as e:
        print("error connecting to Google Sheets\n")
        return df

def main():
    
    df = connect_to_google_sheets()



    print("connect to SAP\n")
    try:
        SapGuiAuto = win32com.client.GetObject("SAPGUI")
        application = SapGuiAuto.GetScriptingEngine
        connection = application.Children(0)
        session = connection.Children(0)

    except Exception as e:
        print(e)
        return

    session.findById("wnd[0]").maximize()
    session.findById("wnd[0]/tbar[0]/okcd").text = "ZMM_UPDATE2"
    session.findById("wnd[0]/tbar[0]/btn[0]").press() 
    session.findById("wnd[0]/usr/ctxtS_SPART-LOW").setFocus()
    session.findById("wnd[0]/usr/ctxtS_SPART-LOW").caretPosition = 0

    print("tested\n")


if __name__ == "__main__":
    main()  