import tkinter as tk
from tkinter import simpledialog
import keyboard
import subprocess
import os


root = tk.Tk()
root.withdraw()  


def selectedNum(num):
    print(f"Function received number: {num}")
    if num == 1:
      subprocess.Popen([r"C:\Riot Games\Riot Client\RiotClientServices.exe"], shell=True)
    elif num == 2:
        os.system("taskkill /f /im LeagueClient.exe")
        os.system("taskkill /f /im League of Legends.exe")
        os.system("taskkill /f /im RiotClientServices.exe")
        for process in processes:
            os.system(f'taskkill /f /im "{process}" >nul 2>&1"')

    elif num == 0:
        root.quit()  

def show_input_box():
    win = tk.Toplevel(root, padx=10, pady=10)
    win.title("Quick Input")
    win.geometry("100x75")
    
    # Force focus and bring to front
    win.lift()
    win.attributes("-topmost", True)
    win.focus_force()
    win.after(10, lambda: win.attributes("-topmost", False))  # Reset topmost so it behaves normally after

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

    
    win.bind("<Return>", lambda event: handle())

    btn = tk.Button(win, text="OK", command=handle)
    btn.pack()

def trigger_popup():
    root.after(0, show_input_box)

keyboard.add_hotkey('shift+f12', trigger_popup)

print("Running... Press Shift + F12 to trigger input.")
root.mainloop()
root.destroy()