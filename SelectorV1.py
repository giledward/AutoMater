import tkinter as tk
from tkinter import ttk
import keyboard
import mouse
import time
from ctypes import windll
import sys
import json
import subprocess
import os
import psutil

class ModernSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        
        # Initialize modes dictionary
        self.modes = {i: False for i in range(10)}
        self.processes = {}
        
        # Load configuration
        self.load_config()
        
        # Set DPI awareness for crisp rendering
        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print("Configuration file not found. Using default settings.")
            self.config = {"modes": {}}

    def create_popup(self):
        # Destroy existing popup if it exists
        if hasattr(self, 'popup') and self.popup.winfo_exists():
            self.popup.destroy()

        # Create new popup
        self.popup = tk.Toplevel(self.root)
        self.popup.overrideredirect(True)  # Remove window decorations
        
        # Calculate center position
        screen_width = self.popup.winfo_screenwidth()
        screen_height = self.popup.winfo_screenheight()
        window_width = 300
        window_height = 60
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.popup.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Create main frame with modern styling
        main_frame = ttk.Frame(self.popup)
        main_frame.pack(fill='both', expand=True)
        
        # Configure modern styles
        style = ttk.Style()
        style.configure("Modern.TEntry", padding=10)
        
        # Create and configure the entry widget
        self.entry = ttk.Entry(main_frame, style="Modern.TEntry", font=('Segoe UI', 12))
        self.entry.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Focus and select all text
        self.entry.focus_force()
        
        # Bind events
        self.entry.bind('<Return>', self.handle_input)
        self.entry.bind('<Escape>', lambda e: self.popup.destroy())
        
        # Make window stay on top
        self.popup.attributes('-topmost', True)
        
        # Add subtle shadow effect
        self.popup.configure(bg='#222222')
        main_frame.configure(style='Modern.TFrame')

    def handle_input(self, event=None):
        try:
            number = int(self.entry.get())
            if 0 <= number <= 9:
                self.execute_action(number)
            else:
                print("Please enter a number between 0-9")
        except ValueError:
            print("Invalid input. Please enter a number.")
        finally:
            self.popup.destroy()

    def execute_action(self, num):
        mode_config = self.config["modes"].get(str(num))
        if not mode_config:
            print(f"No configuration found for mode {num}")
            return

        action_type = mode_config.get("type", "")
        
        if action_type == "exit":
            self.root.quit()
            return
            
        elif action_type == "program":
            programs = mode_config.get("programs", [])
            
            if not programs:
                print(f"No programs configured for mode {num}")
                return
                
            if not self.modes[num]:
                success = True
                for program in programs:
                    program_path = program.get("program_path")
                    if not program_path:
                        continue
                        
                    try:
                        subprocess.Popen(program_path)
                    except Exception as e:
                        print(f"Error launching {program_path}: {e}")
                        success = False
                
                if success:
                    self.modes[num] = True
                    print(f"Launched {mode_config['name']}")
            else:
                for program in programs:
                    process_name = program.get("process_name")
                    if not process_name:
                        continue
                        
                    try:
                        for proc in psutil.process_iter(['name']):
                            if proc.info['name'].lower() == process_name.lower():
                                proc.terminate()
                    except Exception as e:
                        print(f"Error closing {process_name}: {e}")
                
                self.modes[num] = False
                print(f"Closed {mode_config['name']}")
                    
        elif action_type == "autoclicker":
            clicks = mode_config.get("clicks", 19000)
            delay = mode_config.get("delay", 0.00001)
            
            if not self.modes[num]:
                self.modes[num] = True
                print(f"Starting {mode_config['name']}")
                try:
                    time.sleep(1)  # Brief delay before starting
                    for _ in range(clicks):
                        if not self.modes[num]:  # Check if mode was disabled
                            break
                        mouse.click()
                        time.sleep(delay)
                except Exception as e:
                    print(f"Error in auto-clicker: {e}")
            else:
                self.modes[num] = False
                print(f"Stopped {mode_config['name']}")
                
        elif action_type == "script":
            script_path = mode_config.get("script_path")
            if not script_path:
                print(f"Invalid script configuration for mode {num}")
                return
                
            if not self.modes[num]:
                try:
                    subprocess.Popen([sys.executable, script_path])
                    self.modes[num] = True
                    print(f"Started {mode_config['name']}")
                except Exception as e:
                    print(f"Error running script: {e}")
            else:
                self.modes[num] = False
                print(f"Stopped {mode_config['name']}")

    def run(self):
        # Register global hotkey
        keyboard.add_hotkey('shift+f12', self.create_popup, suppress=True)
        print("Running... Press Shift + F12 to open selector.")
        print("\nAvailable modes:")
        for num, mode in self.config["modes"].items():
            print(f"{num}: {mode['name']} - {mode['description']}")
        
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            keyboard.unhook_all()

if __name__ == "__main__":
    selector = ModernSelector()
    selector.run()