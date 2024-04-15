import tkinter as tk
from tkinter import ttk

import subprocess
import sys
import os

try:
    import playsound as playsound
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install","--upgrade", "wheel"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playsound==1.2.2"])
    import playsound as playsound

def generate_request():
    print(f"Request Generated with: {video_var.get()} and {perm_var.get()}")

def cancel():
    window.destroy()

def play():
    if audio_dropdown.get() == "American":
        playsound.playsound(os.path.dirname(__file__) + '\\sample1.mp3')
    elif audio_dropdown.get() == "Australian":
        playsound.playsound(os.path.dirname(__file__) + '\\sample2.mp3')
    else:
        playsound.playsound(os.path.dirname(__file__) + '\\sample3.mp3')

# Create the main window
window = tk.Tk()
window.title("Video and Permutation Selector")

# Set the default size of the window
window.geometry("600x500")  # Increased width to better fit the welcome text

# Configure grid layout
window.columnconfigure(0, weight=1)
window.rowconfigure([0, 1, 2, 3, 4, 5], weight=1)

# Variables for dropdowns
video_var = tk.StringVar()
perm_var = tk.StringVar()
audio_var = tk.StringVar()

# Welcome text label
welcome_text = ("Welcome to our 4P02 final video production tool! This tool was developed in "
                "order to create a video production pipeline to create content for short form "
                "video platforms, as well as deployment and determining what performs well. "
                "Please use the following menus to move forward!")
welcome_label = ttk.Label(window, text=welcome_text, wraplength=550, justify="center")
welcome_label.grid(column=0, row=0, padx=10, pady=10, sticky=tk.EW)

# Video dropdown
video_label = ttk.Label(window, text="Select Video:")
video_label.grid(column=0, row=1, padx=10, pady=5, sticky=tk.W)

video_dropdown = ttk.Combobox(window, textvariable=video_var)
video_dropdown['values'] = ("video 1", "video 2", "video 3")
video_dropdown['state'] = 'readonly'  # Prevent user from typing a value
video_dropdown.grid(column=0, row=2, padx=10, pady=5, sticky=tk.EW)

# Permutation dropdown
perm_label = ttk.Label(window, text="Select Permutation:")
perm_label.grid(column=0, row=3, padx=10, pady=5, sticky=tk.W)

perm_dropdown = ttk.Combobox(window, textvariable=perm_var)
perm_dropdown['values'] = ("permutation 1", "permutation 2", "permutation 3")
perm_dropdown['state'] = 'readonly'
perm_dropdown.grid(column=0, row=4, padx=10, pady=5, sticky=tk.EW)

# Audio dropdown
audio_label = ttk.Label(window, text="Select Voice:")
audio_label.grid(column=0, row=5, padx=10, pady=5, sticky=tk.W)

audio_dropdown = ttk.Combobox(window, textvariable=audio_var)
audio_dropdown['values'] = ("American", "Australian", "British")
audio_dropdown.current(0)
audio_dropdown['state'] = 'readonly'
audio_dropdown.grid(column=0, row=6, padx=10, pady=5, sticky=tk.EW)

audio_preview = ttk.Button(window, text="Sample", command=play)
audio_preview.grid(column=0, row=7, padx=10, pady=10, sticky=tk.E)

# Buttons
cancel_button = ttk.Button(window, text="Cancel", command=cancel)
cancel_button.grid(column=0, row=10, padx=10, pady=10, sticky=tk.E)

generate_button = ttk.Button(window, text="Generate Request", command=generate_request)
generate_button.grid(column=0, row=10, padx=10, pady=10, sticky=tk.W)

# Start the GUI event loop
window.mainloop()

