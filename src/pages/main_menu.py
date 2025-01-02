import customtkinter as ctk
from src.tkreact import render_page
import tkinter as tk

from .fractal_editor import fractal_editor

def main_menu(root, frame):
    # Logic
    def start_button():
        render_page(fractal_editor)

    def quit_button():
        root.destroy()
    
    # UI
    # label = ctk.CTkLabel(master=frame, text="Ready to start the game?", font = ("Aerial", 20))
    # label.place(relx=0.5, rely=0.3, anchor = "n")
    #
    # btn1 = ctk.CTkButton(master=frame, text="Start", command=start_button)
    # btn1.place(relx=0.5, rely=0.5, anchor="center")
    #
    # btn2 = ctk.CTkButton(master=frame, text="Quit", command=quit_button)
    # btn2.place(relx=0.5, rely=0.7, anchor="s")
    frame.pack(pady=20, padx=60, fill="both", expand = True)

    def slider_event(value):
        print(value)

    # to create the blank canvas to draw on
    canvas = tk.Canvas(frame, width=600, height=600, bg="white")
    canvas.place(relx=0.95, rely=0.5, anchor='e')

    # slider from 1 - 100
    slider = ctk.CTkSlider(master=frame, from_ = 0, to = 100, command = slider_event)
    slider.place(relx=0.35, rely=0.8, anchor="se")


    label = ctk.CTkLabel(master=frame, text="Ready to start the game?", font = ("Aerial", 20))
    label.place(relx=0.5, rely=0.3, anchor = "n")

    btn1 = ctk.CTkButton(master=frame, text="Start", command=start_button)
    btn1.place(relx=0.5, rely=0.5, anchor="center")

    btn2 = ctk.CTkButton(master=frame, text="Quit", command=quit_button)
    btn2.place(relx=0.5, rely=0.7, anchor="s")



