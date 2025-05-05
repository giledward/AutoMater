import tkinter as tk
from tkinter import simpledialog
import keyboard

# Global tkinter root
root = tk.Tk()
root.withdraw()  # Hide main window

# Your function that uses the number
def your_function(num):
    print(f"Function received number: {num}")
    root.quit()  # Close the program after use

# The popup input window
def show_input_box():
    win = tk.Toplevel(root)
    win.title("Quick Input")
    win.geometry("250x100")
    win.attributes("-topmost", True)
    win.focus_force()

    entry = tk.Entry(win)
    entry.pack(pady=10)
    entry.focus_set()

    def handle():
        try:
            number = int(entry.get())
            your_function(number)
        except ValueError:
            print("Invalid number.")
        win.destroy()

    # Bind Enter key
    win.bind("<Return>", lambda event: handle())

    btn = tk.Button(win, text="OK", command=handle)
    btn.pack()

# Safe trigger from background
def trigger_popup():
    root.after(0, show_input_box)

# Set hotkey
keyboard.add_hotkey('shift+f12', trigger_popup)

print("Running... Press Shift + F12 to trigger input.")
root.mainloop()
