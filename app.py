import customtkinter as ctk
from customtkinter import filedialog
import threading
from PIL import Image
import os
import shutil
import pandas as pd
import configparser
from logger_setup import get_logger

logger = get_logger(__name__)

class commodity_code_updater_app(ctk.CTk):
    def __init__(self, main_sap_task, main_desc_task):
        super().__init__()
        
        # store status
        self.sap_task = main_sap_task
        self.desc_task = main_desc_task
        self.selected_file_path = None

        # app window setup
        self.geometry("450x400") 
        self.resizable(False, False)

        #display
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # upper panel
        self.iconbitmap("static/hiab.ico")
        self.title("commodity code updater")

        # add photo
        self.logo = ctk.CTkImage(Image.open("static/hiab-text-logo.png"), size=(220, 75))
        self.logo_label = ctk.CTkLabel(self, image=self.logo, text="")
        self.logo_label.pack(pady=(30, 20))

        #BUTTONS 

        # sap button
        self.sap_button = ctk.CTkButton(self, text="Start SAP Automation", command= lambda: self.button_clicked(self.sap_task),
                                     width=320, height=40, font=("Helvetica", 16, "bold"), 
                                     fg_color="#4CAF50", hover_color="#45a049")
        self.sap_button.pack(pady=10)

        # desc button
        self.desc_button = ctk.CTkButton(self, text="Start Scraping Automation", command= lambda: self.button_clicked(self.desc_task),
                                     width=320, height=40, font=("Helvetica", 16, "bold"), 
                                     fg_color="#4CAF50", hover_color="#45a049")
        self.desc_button.pack(pady=10)



        

        self.status_label = ctk.CTkLabel(self, text="Status: Ready to start.", font=("Helvetica", 14))
        self.status_label.pack(pady=10)


        # input file frame
        self.file_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.file_frame.pack(pady=10)

        logger.info("App window ready. Waiting for user to choose a task.")



    def show_skipped_codes(self, skipped):
        """Show materials/codes that were not updated or could not be scraped."""
        popup = ctk.CTkToplevel(self)
        popup.geometry("520x340")
        popup.resizable(True, True)
        popup.iconbitmap("static/hiab.ico")
        popup.title("Skipped rows")
        popup.transient(self)

        ctk.CTkLabel(
            popup,
            text=f"{len(skipped)} item(s) were skipped:",
            font=("Helvetica", 14),
            wraplength=480,
        ).pack(pady=(16, 8), padx=12)

        textbox = ctk.CTkTextbox(popup, width=480, height=220, font=("Helvetica", 12))
        textbox.pack(padx=12, pady=8, fill="both", expand=True)
        lines = []
        for item in skipped:
            material = item.get("material") or ""
            prefix = f"{material} | " if material else ""
            lines.append(f"{prefix}{item['hs_code']} — {item['reason']}")
        textbox.insert("1.0", "\n".join(lines))
        textbox.configure(state="disabled")

        ctk.CTkButton(popup, text="OK", width=100, command=popup.destroy).pack(pady=(4, 16))

    # threading logic (connect with main without freezing ui )
    def run_thread(self, task):
        task_name = getattr(task, "__name__", str(task))
        logger.info("Task thread started: %s", task_name)
        try:
            result = None
            if task:
                result = task() # Execute the stored function
            # handle shipped rows (didnt want to process)
            skipped = result if isinstance(result, list) else None
            if skipped:
                labels = []
                for item in skipped:
                    material = item.get("material") or ""
                    labels.append(material if material else item["hs_code"])
                codes = ", ".join(labels)
                self.status_label.configure(
                    text=f"Finished with {len(skipped)} skipped items",
                    text_color="orange",
                )
                self.after(0, lambda: self.show_skipped_codes(skipped))
                logger.info(
                    "Task finished with warnings: %d items were skipped.",
                    len(skipped),
                )
            else:
                self.status_label.configure(text="Status: Finished successfully!", text_color=["gray10", "gray90"])
                logger.info("Task finished successfully.")
        except Exception as e:
            logger.error("Task stopped with an error (%s): %s", task_name, e, exc_info=True)
            self.status_label.configure(text=f"Error", text_color="red")
            if task == self.sap_task:
                self.status_label.configure(text=f"Error: check if you're in SAP main GUI", text_color="red")
        finally:
            self.sap_button.configure(state="normal")
            self.desc_button.configure(state="normal")
            

    #start -> thread trigger
    def button_clicked(self, task):
        task_name = getattr(task, "__name__", str(task))
        friendly = {
            "main_sap": "SAP automation (update commodity codes in SAP)",
            "main_desc": "Description scraping (EU TARIC website)",
        }.get(task_name, task_name)
        logger.info("")
        logger.info(">>> User started: %s", friendly)
        self.sap_button.configure(state="disabled")
        self.desc_button.configure(state="disabled")
  

        self.status_label.configure(text="Status: Automation running...", text_color=["gray10", "gray90"])

        threading.Thread(target=self.run_thread, args=(task,)).start()
        
