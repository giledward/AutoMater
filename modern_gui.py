import tkinter as tk
from tkinter import ttk
import json
import os
from tkinter import messagebox
import customtkinter as ctk

class ModernGUI:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.root = ctk.CTk()
        self.root.title("AutoMater Control Panel")
        self.root.geometry("800x600")
        
        self.load_config()
        self.create_gui()
        
    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {"modes": {}}
            for i in range(10):
                self.config["modes"][str(i)] = {
                    "name": f"Mode {i}",
                    "description": "Not configured",
                    "type": "program",
                    "programs": []
                }
            self.save_config()

    def save_config(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def create_gui(self):
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            self.main_container,
            text="AutoMater Control Panel",
            font=("Segoe UI", 24, "bold")
        )
        title.pack(pady=10)

        self.mode_frames = {}
        for mode_num in range(10):
            self.create_mode_frame(mode_num)

    def create_mode_frame(self, mode_num):
        mode_config = self.config["modes"].get(str(mode_num), {})
        
        frame = ctk.CTkFrame(self.main_container)
        frame.pack(fill="x", padx=10, pady=5)
        
        header_frame = ctk.CTkFrame(frame)
        header_frame.pack(fill="x", padx=5, pady=5)
        
        mode_label = ctk.CTkLabel(
            header_frame,
            text=f"Mode {mode_num}:",
            font=("Segoe UI", 12, "bold")
        )
        mode_label.pack(side="left", padx=5)
        
        name_var = tk.StringVar(value=mode_config.get("name", f"Mode {mode_num}"))
        name_entry = ctk.CTkEntry(
            header_frame,
            textvariable=name_var,
            width=200
        )
        name_entry.pack(side="left", padx=5)
        
        status = ctk.CTkLabel(
            header_frame,
            text="●",
            text_color="gray",
            font=("Segoe UI", 16)
        )
        status.pack(side="right", padx=5)
        
        desc_var = tk.StringVar(value=mode_config.get("description", "Not configured"))
        desc_entry = ctk.CTkEntry(
            frame,
            textvariable=desc_var,
            width=400
        )
        desc_entry.pack(fill="x", padx=10, pady=5)
        
        def configure_mode():
            self.open_config_window(mode_num)
            
        config_btn = ctk.CTkButton(
            frame,
            text="Configure",
            command=configure_mode
        )
        config_btn.pack(pady=5)
        
        self.mode_frames[mode_num] = {
            "frame": frame,
            "name_var": name_var,
            "desc_var": desc_var,
            "status": status
        }

    def open_config_window(self, mode_num):
        config_window = ctk.CTkToplevel(self.root)
        config_window.title(f"Configure Mode {mode_num}")
        config_window.geometry("600x400")
        
        mode_config = self.config["modes"].get(str(mode_num), {})
        
        type_frame = ctk.CTkFrame(config_window)
        type_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(type_frame, text="Mode Type:").pack(side="left", padx=5)
        
        type_var = tk.StringVar(value=mode_config.get("type", "program"))
        type_options = ["program", "autoclicker", "script"]
        
        type_menu = ctk.CTkOptionMenu(
            type_frame,
            variable=type_var,
            values=type_options
        )
        type_menu.pack(side="left", padx=5)
        
        def save_config():
            self.config["modes"][str(mode_num)] = {
                "name": self.mode_frames[mode_num]["name_var"].get(),
                "description": self.mode_frames[mode_num]["desc_var"].get(),
                "type": type_var.get()
            }
            self.save_config()
            config_window.destroy()
            messagebox.showinfo("Success", "Configuration saved!")
            
        save_btn = ctk.CTkButton(
            config_window,
            text="Save Configuration",
            command=save_config
        )
        save_btn.pack(side="bottom", pady=10)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernGUI()
    app.run() 