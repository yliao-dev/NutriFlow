import os
import customtkinter as ctk
from config import *
from model.data_manager import *

class DataScreen(ctk.CTkFrame):
    def __init__(self, parent, nutrition_view_model):
        super().__init__(parent)
        self.nutrition_view_model = nutrition_view_model
        os.makedirs(LOG_PATH, exist_ok=True)
        self.initialize_ui()
        
    def initialize_ui(self):
        self.grid_rowconfigure(0, weight=3)  # Data detail row
        self.grid_rowconfigure(1, weight=1)  # Data middle row
        self.grid_rowconfigure(2, weight=1)  # Import/Export frame row
        self.grid_columnconfigure(0, weight=1)
        self.create_data_file_detail_frame()
        self.create_data_middle_frame()
        self.create_data_load_frame()
    
    def create_data_file_detail_frame(self):
        self.data_file_detail_frame = ctk.CTkFrame(self)
        self.data_file_detail_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        self.data_file_detail_frame.grid_rowconfigure(0, weight=1)
        self.data_file_detail_frame.grid_columnconfigure(0, weight=1)  
        self.data_file_detail_frame.grid_columnconfigure(1, weight=1)
        self.data_file_detail_frame = ctk.CTkLabel(
                    self,
                    font=("Arial", 16, "bold"),
                    text=f"{self.nutrition_view_model.user_nutrition_model.log_path}",
                    fg_color="transparent", 
                )
        self.data_file_detail_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
    def create_data_middle_frame(self):
        self.data_middle_frame = ctk.CTkFrame(self)
        self.data_middle_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.data_middle_frame.grid_rowconfigure(0, weight=1)
        self.data_middle_frame.grid_columnconfigure(0, weight=1)  
        self.data_middle_frame.grid_columnconfigure(1, weight=1)
        self.data_middle_frame.grid_columnconfigure(2, weight=1)
        self.generate_report_button = ctk.CTkButton(
                    self.data_middle_frame,
                    text="Generate Report\n(All files from nutrition_logs) ",
                    fg_color="#2980B9",
                    hover_color="#2c2c2c",
                    command=self.generate_report
                )
        self.generate_report_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
    def create_data_load_frame(self):
        self.data_load_frame = ctk.CTkFrame(self)
        self.data_load_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.data_load_frame.grid_rowconfigure(0, weight=1)
        self.data_load_frame.grid_columnconfigure(0, weight=1)  
        self.data_load_frame.grid_columnconfigure(1, weight=1)
        self.data_load_frame.grid_columnconfigure(2, weight=1)
        # Create Import Data button
        self.import_button = ctk.CTkButton(self.data_load_frame, text="Import Data\n(Restart Application)", command=self.import_data)
        self.import_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Create Export Data button
        self.export_button = ctk.CTkButton(self.data_load_frame, text="Export Data", command=self.export_data)
        self.export_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Create New Data button
        self.past_data_button = ctk.CTkButton(self.data_load_frame, text="Create New Log\n(Restart Application)", command=self.create_new_data)
        self.past_data_button.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        
    def import_data(self):
        """Allow the user to select and read a CSV file using pandas."""
        if not import_nutrition_data_from_file(self.nutrition_view_model): 
            return
        write_to_user_config(self.nutrition_view_model)
        restart_app()
    
    def export_data(self):
        if not export_nutrition_data_to_file(self.nutrition_view_model):
            return
            
    
    def create_new_data(self):
        new_nutrition_data_to_file(self.nutrition_view_model)
        restart_app()
    
    def generate_report(self):
        timestamp = datetime.now().strftime("%Y-%m-%d")
        new_file_name = f"report_log_{timestamp}.csv"
        file_name = get_unique_filename(new_file_name)
        export_all_logs_to_report(file_name)
    
