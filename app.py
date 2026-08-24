import customtkinter as ctk
from customtkinter import filedialog
import threading
from PIL import Image
import os
import shutil


class commodity_code_updater_app(ctk.CTk):
    def __init__(self, main_sap_task, main_desc_task):
        super().__init__()
        
        # store status
        self.sap_task = main_sap_task
        self.desc_task = main_desc_task
        self.selected_file_path = None

        # app window setup
        self.geometry("450x480") 
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
                                     width=250, height=50, font=("Helvetica", 16, "bold"), 
                                     fg_color="#4CAF50", hover_color="#45a049")
        self.sap_button.pack(pady=10)

        # desc button
        self.desc_button = ctk.CTkButton(self, text="Start Description Scraping Automation", command= lambda: self.button_clicked(self.desc_task),
                                     width=250, height=50, font=("Helvetica", 16, "bold"), 
                                     fg_color="#4CAF50", hover_color="#45a049")
        self.desc_button.pack(pady=10)

        # update data button
        self.update_data_button = ctk.CTkButton(self, text="Start Update Data", 
                                                command=lambda: self.open_file_popup(self.desc_task),
                                                width=250, height=50, font=("Helvetica", 16, "bold"), 
                                                fg_color="#4CAF50", hover_color="#45a049")
        self.update_data_button.pack(pady=10)

        

        self.status_label = ctk.CTkLabel(self, text="Status: Ready to start.", font=("Helvetica", 14))
        self.status_label.pack(pady=10)


        # input file frame
        self.file_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.file_frame.pack(pady=10)



    def open_file_popup(self, task_to_run):



            popup = ctk.CTkToplevel(self)
            popup.geometry("400x200")
            popup.resizable(False, False)
            # upper panel
            popup.iconbitmap("static/hiab.ico")
            popup.title("commodity code updater")
            
            #lock main window while popup is open
            popup.transient(self)
            popup.grab_set()
            
            # reset previous selection
            self.selected_file_path = None


            ctk.CTkLabel(popup, text="Upload Nomenclature EN.xlsx if you want to update the data", font=("Helvetica", 14)).pack(pady=(20, 5))
            
            file_label = ctk.CTkLabel(popup, text="No file selected...", font=("Helvetica", 12))
            file_label.pack(pady=5)

            def browse():
                file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
                if file_path:
                    self.selected_file_path = file_path
                    file_label.configure(text=os.path.basename(file_path))

            


            def apply():
                if not self.selected_file_path:
                    file_label.configure(text="Please select a file first!", text_color="red")
                    return

                # import file to data folder
                target_folder = "data"
                target_filename = "Nomenclature EN.xlsx"
                target_path = os.path.join(target_folder, target_filename)

                try:
                    if os.path.exists(target_path):
                        os.remove(target_path)

                    shutil.copy(self.selected_file_path, target_path)
                    
                    popup.destroy()

                except Exception as e:
                    file_label.configure(text="Error copying file!", text_color="red")
                    print(f"File Error: {e}")


            # BUTTONS
            ctk.CTkButton(popup, text="Browse", command=browse, width=100).pack(side = "left", padx=20)

            ctk.CTkButton(popup, text="Apply", command=apply, width=100).pack(side="left", padx=10)

            ctk.CTkButton(popup, text="Run", command=lambda: task_to_run, width=100).pack(side="left", padx=10)



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
            self.desc_button.configure(state="normal")
            self.update_data_button.configure(state="normal")

    #start -> thread trigger
    def button_clicked(self, task):
        self.sap_button.configure(state="disabled")
        self.desc_button.configure(state="disabled")
        self.update_data_button.configure(state="disabled")

        self.status_label.configure(text="Status: Automation running...")

        threading.Thread(target=self.run_thread, args=(task,)).start()
        
