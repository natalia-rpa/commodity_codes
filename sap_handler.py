import win32com.client
import pyperclip
import time
import pythoncom

def init_sap():

    pythoncom.CoInitialize()

    print("connect to SAP\n")
    try:
        print("get SAPGUI\n")
        SapGuiAuto = win32com.client.GetObject("SAPGUI")
        print("get scripting engine\n")
        application = SapGuiAuto.GetScriptingEngine
        print("get connection\n")
        connection = application.Children(0)
        print("get session\n")
        session = connection.Children(0)
        print("session: ", session)
    except Exception as e:
        print(e)
        print("sap error: ", e)
        raise Exception("sap error")

    session.findById("wnd[0]/tbar[0]/okcd").text = "ZMM_UPDATE2"
    session.findById("wnd[0]/tbar[0]/btn[0]").press() 

    return session


def update_sap(session,group_data,hs_code):
    try:
        group_data['Material'].to_clipboard(index=False, header=False)

        clipboard = pyperclip.paste()
        print("clipboard: ", clipboard)
        # time.sleep(1)
        print("batch button\n")
        session.findById("wnd[0]/usr/btn%_S_MATNR_%_APP_%-VALU_PUSH").press()


        # clear button in multiple selection
        print("clear button\n")
        session.findById("wnd[1]/tbar[0]/btn[16]").press()
    
        # uplad from clickboard
        print("upload from clipboard\n")
        session.findById("wnd[1]/tbar[0]/btn[24]").press()
        #time.sleep(1)

        # exit from clickboard
        print("exit from clipboard\n")
        session.findById("wnd[1]/tbar[0]/btn[8]").press()
        # time.sleep(1)

        # choose plant
        print("choose plant\n")
        session.findById("wnd[0]/usr/ctxtS_WERKS-LOW").text = "FI63"
        session.findById("wnd[0]/usr/chkC_PLANT").selected = True

        # open execute
        print("run execute\n")
        session.findById("wnd[0]/tbar[1]/btn[8]").press()
        time.sleep(3)

        # #catch  status bar    
        # print("catch status bar\n")
        # status_bar = session.findById("wnd[0]/sbar")
        # print("status bar: ", status_bar.text)
        # if ( status_bar.text == "No data found with given inputs"):
        #     print("no data found with given inputs\n")
        #     raise Exception("no data found with given inputs", )

        #select all
        print("select all\n")
        session.findById("wnd[0]/tbar[1]/btn[13]").press()
        time.sleep(1)

        #choose commodity code
        print("choose commodity code\n")
        session.findById("wnd[0]/usr/tabsMAT_MASTER/tabpMAT_MASTER_FC3/ssubMAT_MASTER_SCA:ZMMR_MATERIAL_MASTER_UPD2:0103/cmbZPLANT_LIST_DROPDOWN").key = "CCOD"
        time.sleep(1)
        session.findById("wnd[0]/usr/tabsMAT_MASTER/tabpMAT_MASTER_FC3/ssubMAT_MASTER_SCA:ZMMR_MATERIAL_MASTER_UPD2:0103/ctxtZPLANT_VALUE").text = hs_code
        time.sleep(1)

        #mass change
        print("mass change\n")
        session.findById("wnd[0]/usr/tabsMAT_MASTER/tabpMAT_MASTER_FC3/ssubMAT_MASTER_SCA:ZMMR_MATERIAL_MASTER_UPD2:0103/btnMASSCHANGE").press()

        #update
        print("update\n")
        session.findById("wnd[0]/tbar[1]/btn[29]").press()

        #back
        print("back from execute\n")
        session.findById("wnd[0]/tbar[0]/btn[3]").press()

    except Exception as e:
        print("sap error")
        raise Exception("sap error")

    return True
