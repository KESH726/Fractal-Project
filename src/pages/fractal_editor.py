import customtkinter as ctk
import tkinter as tk

from src.citysimulation import city

def fractal_editor(root, frame):
    def slider_event(value):
        print(value)

    def start_city():
        root.destroy()
        city.init_city(1000, 720, 1)

    # to create the blank canvas to draw on
    canvas = tk.Canvas(frame, width=600, height=600, bg="white")
    canvas.place(relx=0.95, rely=0.4, anchor='e')

    # slider from 1 - 100
    slider = ctk.CTkSlider(master=frame, from_=0, to=100, command=slider_event)
    slider.place(relx=0.35, rely=0.6, anchor="se")

    btn2 = ctk.CTkButton(master=frame, text="Start city simulation", command=start_city)
    btn2.place(relx=0.5, rely=0.9, anchor="s")