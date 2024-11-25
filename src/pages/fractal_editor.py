import customtkinter as ctk
import pygame

from src.citysimulation import fractal

def fractal_editor(root, frame):
    def start_simulation():
        root.destroy()
        fractal.main(1, 800, 800, 4, 0.5)

    label = ctk.CTkLabel(master=frame, text="Fractal Editor", font = ("Aerial", 20))
    label.place(relx=0.5, rely=0.3, anchor = "n")

    btn1 = ctk.CTkButton(master=frame, text="Start city simulation", command=start_simulation)
    btn1.place(relx=0.5, rely=0.5, anchor="center")