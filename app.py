import customtkinter as ctk
import threading

# ==========================================
# 1. APP WINDOW SETUP
# ==========================================
app = ctk.CTk()
app.title("SAP Commodity Code Updater")
app.geometry("650x600")
app.resizable(False, False)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Global variable to hold the logic passed from main.py
automation_task = None 

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
def log_message(message):
    """Prints messages to the UI terminal"""
    print(message) 
    log_box.configure(state="normal")
    log_box.insert("end", message + "\n")
    log_box.see("end") 
    log_box.configure(state="disabled")

# ==========================================
# 3. THREADING LOGIC
# ==========================================
def run_thread():
    """Runs the injected workflow without freezing the UI"""
    try:
        if automation_task:
            # We pass the log_message function to main.py so it can talk to the UI
            automation_task(log_message) 
            
        status_label.configure(text="Status: Finished successfully!")
    except Exception as e:
        log_message(f"\nCRITICAL ERROR: {str(e)}")
        status_label.configure(text="Status: Process failed with errors.")
    finally:
        start_button.configure(state="normal")

def start_clicked():
    """Triggered when the green Start button is pressed"""
    start_button.configure(state="disabled")
    status_label.configure(text="Status: Automation running...")
    
    log_box.configure(state="normal")
    log_box.delete("1.0", "end")
    log_box.configure(state="disabled")
    
    threading.Thread(target=run_thread).start()

# ==========================================
# 4. BUILD THE UI (Widgets)
# ==========================================
title_label = ctk.CTkLabel(app, text="SAP Commodity Code Updater", font=("Helvetica", 24, "bold"))
title_label.pack(pady=(30, 10))

start_button = ctk.CTkButton(app, text="Start Automation", command=start_clicked,
                             width=250, height=50, font=("Helvetica", 16, "bold"), 
                             fg_color="#4CAF50", hover_color="#45a049")
start_button.pack(pady=10)

status_label = ctk.CTkLabel(app, text="Status: Ready to start.", font=("Helvetica", 14))
status_label.pack(pady=5)

log_frame = ctk.CTkFrame(app)
log_frame.pack(pady=10, padx=40, fill="both", expand=True)

log_label = ctk.CTkLabel(log_frame, text="Activity Log:", font=("Helvetica", 12, "bold"))
log_label.pack(anchor="w", padx=10, pady=(10, 0))

log_box = ctk.CTkTextbox(log_frame, font=("Consolas", 12), state="disabled")
log_box.pack(pady=10, padx=10, fill="both", expand=True)

# ==========================================
# 5. EXPORT THE UI LAUNCHER
# ==========================================
def start_ui(workflow_function):
    """Called by main.py to start the app and inject the logic"""
    global automation_task
    automation_task = workflow_function
    app.mainloop()