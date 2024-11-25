import customtkinter as ctk
import pygame

from src.citysimulation import fractal
from src.citysimulation import city

def fractal_editor(root, frame):
    def start_fractal():
        root.destroy()
        fractal.main(1, 800, 800, 4, 0.5)

    def start_city():
        root.destroy()
        city.init_city(800, 800, 1)


    label = ctk.CTkLabel(master=frame, text="Fractal City", font = ("Aerial", 20))
    label.place(relx=0.5, rely=0.3, anchor = "n")

    btn1 = ctk.CTkButton(master=frame, text="Draw fractal", command=start_fractal)
    btn1.place(relx=0.5, rely=0.5, anchor="center")

    btn2 = ctk.CTkButton(master=frame, text="Start city simulation", command=start_city)
    btn2.place(relx=0.5, rely=0.6, anchor="center")