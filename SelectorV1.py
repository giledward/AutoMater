import tkinter as tk
from tkinter import simpledialog
import keyboard
import subprocess
import os
from selenium import webdriver

root = tk.Tk()
root.withdraw()  

modes = {
        1: False, 2: False, 3: False, 4: False, 5: False,
        6: False, 7: False, 8: False, 9: False, 0: False
    }


def selectedNum(num):
    if num == 1:
        if  modes[1]== False:
            response = ("Prende")
            print(response)
            modes[1] = True
        else:
            modes[1] = False
            response = ("apaga")
            print(response)
    elif num == 2:
        if  modes[2]== False:
            response = ("Prende")
            print(response)
            modes[2] = True
        else:
            modes[2] = False
            response = ("apaga")
            print(response)
    elif num == 3:
        if  modes[3]== False:
            response = ("Prende")
            print(response)
            modes[3] = True
        else:
            modes[3] = False
            response = ("apaga")
            print(response)
    elif num == 4:
        if  modes[4]== False:
            response = ("Prende")
            print(response)
            modes[4] = True
        else:
            modes[4] = False
            response = ("apaga")
            print(response)
    elif num == 5:
        if  modes[5]== False:
            response = ("Prende")
            print(response)
            modes[5] = True
        else:
            modes[5] = False
            response = ("apaga")
            print(response) 
    elif num == 6:
        if  modes[6]== False:
            response = ("Prende")
            print(response)
            modes[6] = True
        else:
            modes[6] = False
            response = ("apaga")
            print(response)
    elif num == 7:
        if  modes[7]== False:
            response = ("Prende")
            print(response)
            modes[7] = True
        else:
            modes[7] = False
            response = ("apaga")
            print(response)    
    elif num == 8:
        if  modes[8]== False:
            response = ("Prende")
            print(response)
            modes[8] = True
        else:
            modes[8] = False
            response = ("apaga")
            print(response)
    elif num == 9:
        if  modes[9]== False:
            response = ("Prende")
            print(response)
            modes[9] = True
        else:
            modes[9] = False
            response = ("apaga")
            print(response)
            
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