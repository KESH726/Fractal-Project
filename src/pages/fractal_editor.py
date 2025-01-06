import customtkinter as ctk
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

from src.citysimulation import city
from src.services.FractalGenerator import FractalGenerator

fractal_generator = FractalGenerator()



def mapcolor(iterations, max_iteration):
    colormap = (255 - iterations * 255 // max_iteration).astype(np.uint8)
    return np.stack([colormap, colormap // 2, colormap // 4], axis=-1)

def fractal_editor(root, frame):
    canvas = tk.Canvas(frame, width=600, height=600, bg="white")
    canvas.place(relx=0.95, rely=0.4, anchor='e')
    
    def update_canvas():
        fractals = fractal_generator.generate_fractal().fractal_pixels
        print("Fractal generation done")
        colors = mapcolor(fractals, fractal_generator.max_iteration)
        img = Image.fromarray(colors, mode="RGB")
        image_ = ImageTk.PhotoImage(img)
        
        # img.show()

        canvas.create_image(100,100,anchor="center",image=image_)
        
        canvas.update()
        
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

    # to create the blank canvas to draw on
    update_canvas()

    # slider from 1 - 100
    x_label = ctk.CTkLabel(master=frame, text="Values for x")
    # x_label.grid(row = 0, colmun = 0)
    slider = ctk.CTkSlider(master=frame, from_=-2, to=2, command=slider_event_x)
    slider.place(relx=0.35, rely=0.6, anchor="se")
    
    slider = ctk.CTkSlider(master=frame, from_=-2, to=2, command=slider_event_i)
    slider.place(relx=0.35, rely=0.7, anchor="se")

    btn2 = ctk.CTkButton(master=frame, text="Start city simulation", command=start_city)
    btn2.place(relx=0.5, rely=0.9, anchor="s")