import customtkinter as ctk
import tkinter as tk


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.geometry("960x600")
name = root.title("Recursive graphics project")

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand = True)

# to create the slider 
def slider_event(value):
    print(value)

# to create the blank canvas to draw on
canvas = tk.Canvas(frame, width=400, height=600, bg="white")
canvas.place(relx=0.95, rely=0.5, anchor='e')

# slider from 1 - 100
slider = ctk.CTkSlider(master=frame, from_ = 0, to = 100, command = slider_event)
slider.place(relx=0.35, rely=0.8, anchor="se")

root.mainloop()
