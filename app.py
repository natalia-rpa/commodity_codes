import customtkinter as ctk
import threading
from PIL import Image



class commodity_code_updater_app(ctk.CTk):
    def __init__(self, main_sap_task, main_desc_task):
        super().__init__()
        
        # store status
        self.sap_task = main_sap_task
        self.desc_task = main_desc_task


        # app window setup
        self.geometry("450x250") 
        self.resizable(False, False)

        #display
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # upper label
        self.iconbitmap("static/hiab.ico")
        self.title("commodity code updater")

        # add photo
        self.logo = ctk.CTkImage(Image.open("static/hiab-text-logo.png"), size=(220, 75))
        self.logo_label = ctk.CTkLabel(self, image=self.logo, text="")
        self.logo_label.pack(pady=(30, 20))

        #title
        # self.title_label = ctk.CTkLabel(self, text="zmmmzmz", font=("Helvetica", 24, "bold"))
        # self.title_label.pack(pady=(30, 20))


        # sap button
        self.sap_button = ctk.CTkButton(self, text="Start SAP Automation", command=self.sap_button_clicked,
                                     width=250, height=50, font=("Helvetica", 16, "bold"), 
                                     fg_color="#4CAF50", hover_color="#45a049")
        self.sap_button.pack(pady=10)

        # desc button
        self.desc_button = ctk.CTkButton(self, text="Start Description Scraping Automation", command=self.desc_button_clicked,
                                     width=250, height=50, font=("Helvetica", 16, "bold"), 
                                     fg_color="#4CAF50", hover_color="#45a049")
        self.desc_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Status: Ready to start.", font=("Helvetica", 14))
        self.status_label.pack(pady=10)

    # threading logic (connect with main without freezing ui )
    def run_thread(self, task):
        try:
            if task:
                task() # Execute the stored function
                
            self.status_label.configure(text="Status: Finished successfully!")
        except Exception as e:
            print(f"CRITICAL ERROR: {str(e)}")
            self.status_label.configure(text="Status: Process failed with errors.")
        finally:
            self.sap_button.configure(state="normal")

    #start -> thread trigger
    def sap_button_clicked(self):
        self.sap_button.configure(state="disabled")
        self.status_label.configure(text="Status: Automation running...")

        threading.Thread(target=self.run_thread, args=(self.sap_task,)).start()
        


    def desc_button_clicked(self):
        self.desc_button.configure(state="disabled")
        self.status_label.configure(text="Status: Automation running...")

        threading.Thread(target=self.run_thread, args=(self.desc_task,)).start()

# if desc_button_clicked the other main.py (eg main2) logic will start .how to do it and it is a good idea?