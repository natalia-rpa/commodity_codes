import customtkinter as ctk
import threading
from PIL import Image



class commodity_code_updater_app(ctk.CTk):
    def __init__(self, main):
        super().__init__()
        
        # store status
        self.automation_task = main
        
        # app window setup

        
        
        self.geometry("450x250") 
        self.resizable(False, False)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # build the ui
        self.iconbitmap("static/hiab.ico")
        self.title("commodity code updater")

        # add photo
        self.logo = ctk.CTkImage(Image.open("static/hiab-text-logo.png"), size=(220, 75))
        self.logo_label = ctk.CTkLabel(self, image=self.logo, text="")
        self.logo_label.pack(pady=(30, 20))

        # self.title_label = ctk.CTkLabel(self, text="zmmmzmz", font=("Helvetica", 24, "bold"))
        # self.title_label.pack(pady=(30, 20))

        self.start_button = ctk.CTkButton(self, text="Start Automation", command=self.start_clicked,
                                     width=250, height=50, font=("Helvetica", 16, "bold"), 
                                     fg_color="#4CAF50", hover_color="#45a049")
        self.start_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Status: Ready to start.", font=("Helvetica", 14))
        self.status_label.pack(pady=10)

    # threading logic
    def run_thread(self):
        """Runs the injected workflow without freezing the UI"""
        try:
            if self.automation_task:
                self.automation_task() # Execute the stored function
                
            self.status_label.configure(text="Status: Finished successfully!")
        except Exception as e:
            print(f"CRITICAL ERROR: {str(e)}")
            self.status_label.configure(text="Status: Process failed with errors.")
        finally:
            self.start_button.configure(state="normal")

    def start_clicked(self):
        """Triggered when the green Start button is pressed"""
        self.start_button.configure(state="disabled")
        self.status_label.configure(text="Status: Automation running...")
        
        threading.Thread(target=self.run_thread).start()