import tkinter as tk
from tkinter import simpledialog
import keyboard

root = tk.Tk()
root.withdraw()  


def selectedNum(num):
    print(f"Function received number: {num}")
    root.quit()  

def show_input_box():
    win = tk.Toplevel(root, padx=10, pady=10)
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
            selectedNum(number)
        except ValueError:
            print("Invalid number.")
        win.destroy()

    
    win.bind("<Return>", lambda event: handle())

    btn = tk.Button(win, text="OK", command=handle)
    btn.pack()

def trigger_popup():
    root.after(0, show_input_box)

keyboard.add_hotkey('shift+f12', trigger_popup)

print("Running... Press Shift + F12 to trigger input.")
root.mainloop()
