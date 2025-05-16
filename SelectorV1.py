import tkinter as tk
from tkinter import ttk
import keyboard
import mouse
import time
from ctypes import windll
import sys

class ModernSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        
        # Initialize modes dictionary
        self.modes = {i: False for i in range(10)}
        
        # Set DPI awareness for crisp rendering
        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass

    def create_popup(self):
        # Destroy existing popup if it exists
        try:
            if hasattr(self, 'popup') and self.popup.winfo_exists():
                self.popup.destroy()
        except:
            pass

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
        if num == 0:
            self.root.quit()
            return

        self.modes[num] = not self.modes[num]
        state = "activated" if self.modes[num] else "deactivated"
        print(f"Mode {num} {state}")

        # Special action for mode 3 (auto-clicker)
        if num == 3 and self.modes[num]:
            try:
                time.sleep(1)  # Brief delay before starting
                for _ in range(19000):
                    if not self.modes[num]:  # Check if mode was disabled
                        break
                    mouse.click()
                    time.sleep(0.00001)
            except Exception as e:
                print(f"Error in auto-clicker: {e}")

    def run(self):
        # Register global hotkey
        keyboard.add_hotkey('shift+f12', self.create_popup, suppress=True)
        print("Running... Press Shift + F12 to open selector.")
        
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            keyboard.unhook_all()

if __name__ == "__main__":
    selector = ModernSelector()
    selector.run()