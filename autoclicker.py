import ctypes
import time as t
import threading
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import keyboard

# constants
MINDELAY = 5

# variables
clicking = False
delay = 100
click = "left"
keybind = "F6"
keyFlag = False

# functions
def toggleClick():
    global clicking

    if not keyFlag:
        clicking = not clicking
        if clicking:
            threading.Thread(target=clickLoop, daemon=True).start()
            startBtn.config(state="disabled")
            stopBtn.config(state="normal")
        else:
            startBtn.config(state="normal")
            stopBtn.config(state="disabled")

def clickLoop():
    global clicking
    
    nt = t.perf_counter()

    while clicking:
        if click == "left":
            ctypes.windll.user32.mouse_event(2) # left down
            ctypes.windll.user32.mouse_event(4) # Left up
        elif click == "right":
            ctypes.windll.user32.mouse_event(8) # right down
            ctypes.windll.user32.mouse_event(16) # right up
        elif click == "middle":
            ctypes.windll.user32.mouse_event(32) # middle down
            ctypes.windll.user32.mouse_event(64) # middle up
        
        nt += delay / 1000
        t.sleep(max(0, nt - t.perf_counter()))

def updateDelay():
    global delay
    
    try:
        delay = int(delayEntry.get())
        if delay < MINDELAY:
            delay = MINDELAY
            delayEntry.delete(0, tk.END)
            delayEntry.insert(0, str(MINDELAY))
        ecps.config(text=f"Estimated CPS: ~{round(1000 / delay, 2)}")
    except ValueError:
        delayEntry.delete(0, 'end')
        delayEntry.insert(0, str(delay))
        
def updateClickButton(event):
    global click
    
    click = clickMenu.get().lower()

def onKeyPress(event):
    global keybind
    
    if keyFlag:
        keybind = event.name
        keybindEntry.delete(0, tk.END)
        keybindEntry.insert(0, keybind.upper())
        keybindEntry.selection_clear()
        keyboard.remove_all_hotkeys()
        keyboard.add_hotkey(keybind.upper(), toggleClick)
        r.focus()
    
def setKeyFlag(val):
    global keyFlag
    
    keyFlag = val

def onKeyFocus():
    setKeyFlag(True)
    keyboard.on_press(onKeyPress)

# root window
r = ThemedTk(theme="equilux")
r.title("Auto Clicker")
r.geometry("440x260")
r.resizable(False, False)
r.configure(bg="#464646")
r.attributes("-topmost", 1)
r.iconbitmap("icon.ico")

# title label
titleLabel = ttk.Label(r, text="Auto Clicker", font=("Roboto", 12), background="#464646", foreground="#a6a6a6")
titleLabel.pack(pady=(10, 0))

# estimated cps label
ecps = ttk.Label(r, text=f"Estimated CPS: ~{round(1000 / delay, 2)}", font=("Roboto", 10), background="#464646", foreground="#a6a6a6")
ecps.pack()

# main frame
mFr = ttk.Frame(r)

# frame for buttons
btnFr = ttk.Frame(mFr)
btnFr.pack(pady=(0, 5))

# start and stop buttons
startBtn = ttk.Button(btnFr, 
             text="Start", 
             width=10,
             command=toggleClick)
startBtn.pack(side="left", padx=10)

stopBtn = ttk.Button(btnFr, 
             text="Stop", 
             width=10,
             command=toggleClick,
             state="disabled")
stopBtn.pack(side="left", padx=10)

# frame for click type selection
clickFr = ttk.Frame(mFr)
clickFr.pack(pady=(5, 0))

# click type dropdown
clickLabel = ttk.Label(clickFr, text="Click Type:")
clickLabel.pack(side="left")

clickMenu = ttk.Combobox(clickFr, values=["Left", "Right", "Middle"], state="readonly", width=10)
clickMenu.set("Left")
clickMenu.pack(side="left", padx=10)
clickMenu.bind("<<ComboboxSelected>>", updateClickButton)

# frame for delay input
dlyFr = ttk.Frame(mFr)
dlyFr.pack(pady=(5, 0))

# delay input and update delay buttons
delayLabel = ttk.Label(dlyFr, text="Delay (ms):")
delayLabel.pack(side="left")

delayEntry = ttk.Entry(dlyFr, width=10)
delayEntry.insert(0, str(delay))
delayEntry.pack(side="left", padx=10)

updateBtn = ttk.Button(dlyFr, 
             text="Update Delay", 
             width=15, 
             command=updateDelay)
updateBtn.pack(side="left")

# frame for keybind selection
keybindFr = ttk.Frame(mFr)
keybindFr.pack(pady=(5, 0))

keybindLabel = ttk.Label(keybindFr, text="Start/Stop Key:")
keybindLabel.pack(side="left")

keybindEntry = ttk.Entry(keybindFr, width=10)
keybindEntry.insert(0, keybind)
keybindEntry.pack(side="left", padx=10)
keybindEntry.bind("<FocusIn>", lambda e: onKeyFocus())
keybindEntry.bind("<FocusOut>", lambda e: setKeyFlag(False))

# center main frame
mFr.place(relx=0.5, rely=0.5, anchor="c")

# credits label
creditsLabel = ttk.Label(r, text="Made by Nayif E. | v1.0.1", font=("Roboto", 8), background="#464646", foreground="#747474")
creditsLabel.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-5)  # Bottom-right corner with slight padding

# listen to default key press
keyboard.add_hotkey(keybind, toggleClick)

# main window loop
r.mainloop()
