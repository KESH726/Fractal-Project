import customtkinter as ctk
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

from src.citysimulation import city
from src.services.FractalGenerator import FractalGenerator

fractal_generator = FractalGenerator()



def mapcolor(iterations, max_iteration):
    colormap = (255 - iterations * 255 // max_iteration).astype(np.uint8)
    return np.stack([colormap, colormap, colormap], axis=-1)


def fractal_editor(root, frame):
    canvas = tk.Canvas(frame, width=900, height=600, bg="white")
    canvas.place(relx=0.95, rely=0.4, anchor='e')
    slider_grp = ctk.CTkFrame(master=frame,bg_color="white", height=130,width=200)
    x_label = ctk.CTkLabel(master=slider_grp, text=f"X = {fractal_generator.x}", font = ("Aerial", 10))
    i_label = ctk.CTkLabel(master=slider_grp, text=f"I = {fractal_generator.i}", font = ("Aerial", 10))
    
   
    def update_canvas():
        fractals = fractal_generator.generate_fractal().fractal_pixels
        print("Fractal generation done")
        
        colors = mapcolor(fractals, fractal_generator.max_iteration)
        img = Image.fromarray(colors, mode="RGB")
        
        canvas.image = ImageTk.PhotoImage(img)  
        
        canvas.create_image(450, 300, anchor="center", image=canvas.image) 
        x_label.configure(text=f"X = {fractal_generator.x:.2f}")
        i_label.configure(text=f"I = {fractal_generator.i:.2f}")

        
    def slider_event_x(value):
        print(value)
        fractal_generator.set_x(value)
        update_canvas()
        

    def slider_event_i(value):
            print(value)
            fractal_generator.set_i(value)
            update_canvas()
            
    def start_city():
        root.destroy()
        city.init_city(1000, 720, 1)

    # update the canvas for the first time
    update_canvas()

    
    
    slider_grp.place(relx=0.70, rely=0.81, anchor="sw")
    
    x_label.place(relx=0.40, rely=0.2, anchor = "sw")
    
    slider = ctk.CTkSlider(master=slider_grp, from_=-2, to=2, command=slider_event_x)
    slider.place(relx=0.50, rely=0.3, anchor="center")
    
    
    i_label.place(relx=0.40, rely=0.7, anchor = "sw")
    
    slider = ctk.CTkSlider(master=slider_grp, from_=-2, to=2, command=slider_event_i)
    slider.place(relx=0.50, rely=0.8, anchor="center")

    btn2 = ctk.CTkButton(master=frame, text="Start city simulation", command=start_city)
    btn2.place(relx=0.5, rely=0.9, anchor="s")