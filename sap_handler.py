import win32com.client
import pyperclip
import time
import pythoncom
from logger_setup import get_logger

logger = get_logger(__name__)




def init_sap():

    pythoncom.CoInitialize()

    logger.info("Connecting to the open SAP GUI window...")
    try:
        SapGuiAuto = win32com.client.GetObject("SAPGUI")
        application = SapGuiAuto.GetScriptingEngine
        connection = application.Children(0)
        session = connection.Children(0)
        logger.info("Connected to SAP successfully.")
    except Exception as e:
        logger.error(
            "Could not connect to SAP. Make sure SAP GUI is open on the main screen. Details: %s",
            e,
            exc_info=True,
        )
        raise Exception("sap error")

    logger.info("Opening SAP transaction ZMM_UPDATE2 (material mass update)...")
    session.findById("wnd[0]/tbar[0]/okcd").text = "ZMM_UPDATE2"
    session.findById("wnd[0]/tbar[0]/btn[0]").press() 
    logger.info("Transaction ZMM_UPDATE2 is open.")

    return session


def update_sap(session,group_data,hs_code):
    material_count = len(group_data)
    try:
        logger.info(
            "SAP update for HS CODE %s — selecting %d material(s) for plant FI63...",
            hs_code,
            material_count,
        )
        group_data['Material'].to_clipboard(index=False, header=False)

        clipboard = pyperclip.paste()
        logger.debug("Materials copied to clipboard: %s", clipboard)
        #time.sleep(1)
        session.findById("wnd[0]/usr/btn%_S_MATNR_%_APP_%-VALU_PUSH").press()


        # clear button in multiple selection
        session.findById("wnd[1]/tbar[0]/btn[16]").press()
        #time.sleep(1)

        # upload from clickboard
        session.findById("wnd[1]/tbar[0]/btn[24]").press()
        #time.sleep(2)

        # exit from clickboard
        session.findById("wnd[1]/tbar[0]/btn[8]").press()
        #time.sleep(2)

        # choose plant
        session.findById("wnd[0]/usr/ctxtS_WERKS-LOW").text = "FI63"
        session.findById("wnd[0]/usr/chkC_PLANT").selected = True
        #time.sleep(2)
        # open execute
        session.findById("wnd[0]/tbar[1]/btn[8]").press()
        #time.sleep(2)

        #catch  status bar    
        status_bar = session.findById("wnd[0]/sbar")
        logger.info("SAP status after search: %s", status_bar.text or "(empty)")
        if ( status_bar.text == "No data found with given inputs"):
            logger.warning(
                "No materials found in SAP for HS CODE %s (plant FI63). This group will be skipped.",
                hs_code,
            )
            session.findById("wnd[0]/tbar[0]/btn[3]").press()
            return False, "No data found with given inputs"

        #select all
        session.findById("wnd[0]/tbar[1]/btn[13]").press()
       # time.sleep(2)

        #choose commodity code
        logger.info("Setting commodity code to %s ", hs_code)
        session.findById("wnd[0]/usr/tabsMAT_MASTER/tabpMAT_MASTER_FC3/ssubMAT_MASTER_SCA:ZMMR_MATERIAL_MASTER_UPD2:0103/cmbZPLANT_LIST_DROPDOWN").key = "CCOD"
        #time.sleep(2)
        session.findById("wnd[0]/usr/tabsMAT_MASTER/tabpMAT_MASTER_FC3/ssubMAT_MASTER_SCA:ZMMR_MATERIAL_MASTER_UPD2:0103/ctxtZPLANT_VALUE").text = hs_code
        #time.sleep(2)

        #mass change
        session.findById("wnd[0]/usr/tabsMAT_MASTER/tabpMAT_MASTER_FC3/ssubMAT_MASTER_SCA:ZMMR_MATERIAL_MASTER_UPD2:0103/btnMASSCHANGE").press()
       # time.sleep(2)
 
        #update
        session.findById("wnd[0]/tbar[1]/btn[29]").press()

        status_bar = session.findById("wnd[0]/sbar")
        logger.info("SAP status after update: %s", status_bar.text or "(empty)")
        if ( status_bar.text == "Please check error log"):
            logger.error(
                "SAP rejected the update for HS CODE %s (status: Please check error log). "
                "Often the commodity code is invalid. This group will be skipped.",
                hs_code,
            )
            session.findById("wnd[0]/tbar[0]/btn[3]").press()
            return False, "Please check error log (material not updated)"

       # time.sleep(2)
        #back
        session.findById("wnd[0]/tbar[0]/btn[3]").press()
       # time.sleep(2)

    except Exception as e:
        logger.error(
            "Unexpected SAP error while updating HS CODE %s: %s",
            hs_code,
            e,
            exc_info=True,
        )
        raise Exception("sap error")

    logger.info("SAP update succeeded for HS CODE %s (%d material(s)).", hs_code, material_count)
    return True, None
