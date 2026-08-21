import pandas as pd
import spreadsheet_handler
import sap_handler 
import customtkinter as ctk
#import app


def main():
    
    #app.mainloop()
    
    group_df, sheet = spreadsheet_handler.connect_to_google_sheets()

    session = sap_handler.init_sap()

    for _, group_data in group_df:
        sap_handler.update_sap(session, group_data)
        spreadsheet_handler.update_google_sheets(group_data, sheet)





if __name__ == "__main__":
    main()  

    # commodity_col_index = 7 
 
    # print("final HS CODE: ", group_df['final HS CODE'])
    # print("connect to SAP\n")
    # try:
    #     SapGuiAuto = win32com.client.GetObject("SAPGUI")
    #     application = SapGuiAuto.GetScriptingEngine
    #     connection = application.Children(0)
    #     session = connection.Children(0)
    # except Exception as e:
    #     print(e)
    #     return

    # session.findById("wnd[0]/tbar[0]/okcd").text = "ZMM_UPDATE2"
    # session.findById("wnd[0]/tbar[0]/btn[0]").press() 

    # try:
    #     for hs_code, group_data in group_df:
    #         print("updating HS Code: ", hs_code)
    #         print("batch button\n")
    #         session.findById("wnd[0]/usr/btn%_S_MATNR_%_APP_%-VALU_PUSH").press()


    #         group_data['Material'].to_clipboard(index=False, header=False)

    #         clipboard = pyperclip.paste()
    #         print("clipboard: ", clipboard)
    #        # time.sleep(1)


    #         # clear button in multiple selection
    #         print("clear button\n")
    #         session.findById("wnd[1]/tbar[0]/btn[16]").press()
        
    #         # uplad from clickboard
    #         print("upload from clipboard\n")
    #         session.findById("wnd[1]/tbar[0]/btn[24]").press()
    #         #time.sleep(1)

    #         # exit from clickboard
    #         print("exit from clipboard\n")
    #         session.findById("wnd[1]/tbar[0]/btn[8]").press()
    #        # time.sleep(1)

    #         # choose plant
    #         print("choose plant\n")
    #         session.findById("wnd[0]/usr/ctxtS_WERKS-LOW").text = "FI63"
    #         session.findById("wnd[0]/usr/chkC_PLANT").selected = True

    #         # open execute
    #         print("run execute\n")
    #         session.findById("wnd[0]/tbar[1]/btn[8]").press()
    #         time.sleep(3)

    #         #catch  status bar    
    #         print("catch status bar\n")
    #         status_bar = session.findById("wnd[0]/sbar")
    #         print("status bar: ", status_bar.text)
    #         if ( status_bar.text == "No data found with given inputs"):
    #             print("no data found with given inputs\n")
    #             continue

    #         #select all
    #         print("select all\n")
    #         session.findById("wnd[0]/tbar[1]/btn[13]").press()
    #         time.sleep(1)

    #         #choose commodity code
    #         print("choose commodity code\n")
    #         session.findById("wnd[0]/usr/tabsMAT_MASTER/tabpMAT_MASTER_FC3/ssubMAT_MASTER_SCA:ZMMR_MATERIAL_MASTER_UPD2:0103/cmbZPLANT_LIST_DROPDOWN").key = "CCOD"
    #         time.sleep(1)
    #         session.findById("wnd[0]/usr/tabsMAT_MASTER/tabpMAT_MASTER_FC3/ssubMAT_MASTER_SCA:ZMMR_MATERIAL_MASTER_UPD2:0103/ctxtZPLANT_VALUE").text = hs_code
    #         time.sleep(1)

    #         #mass change
    #         print("mass change\n")
    #         session.findById("wnd[0]/usr/tabsMAT_MASTER/tabpMAT_MASTER_FC3/ssubMAT_MASTER_SCA:ZMMR_MATERIAL_MASTER_UPD2:0103/btnMASSCHANGE").press()

    #         #update
    #         print("update\n")
    #         session.findById("wnd[0]/tbar[1]/btn[29]").press()

    #         #back
    #         print("back from execute\n")
    #         session.findById("wnd[0]/tbar[0]/btn[3]").press()


    #         print("updating Google Sheets")
    #         cells_to_update = []
            

    #         for index, row_data in group_data.iterrows():
    #             sheet_row = row_data['sheet_row']
                
    #             cells_to_update.append(gspread.Cell(row=sheet_row, col=commodity_col_index, value=hs_code))
            
    #         # push changes
    #         sheet.update_cells(cells_to_update, value_input_option='USER_ENTERED')
    #         print(f"sheets updated: {len(cells_to_update)} rows changed to {hs_code}\n")




    # except Exception as e:
    #     print("error")
    #     return


