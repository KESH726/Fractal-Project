import customtkinter as ctk
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

from src.citysimulation import city
from src.services.FractalGenerator import FractalGenerator
from collections import defaultdict

fractal_generator = FractalGenerator()

def mapcolor(iterations, max_iteration):
    colormap = (255 - iterations * 255 // max_iteration).astype(np.uint8)
    return np.stack([colormap, colormap, colormap], axis=-1)

def fractal_editor(root, frame):
    canvas = tk.Canvas(frame, width=900, height=600, bg="white")
    canvas.place(relx=0.95, rely=0.4, anchor='e')
    
    slider_grp = ctk.CTkFrame(master=frame, bg_color="white", height=130, width=200)
    x_label = ctk.CTkLabel(master=slider_grp, text=f"X = {fractal_generator.x}", font=("Arial", 10))
    i_label = ctk.CTkLabel(master=slider_grp, text=f"I = {fractal_generator.i}", font=("Arial", 10))
    
    input_grp = ctk.CTkFrame(master=frame, bg_color="white", height=130, width=200)
    seg_len = ctk.CTkEntry(master=input_grp, placeholder_text="Segment Length")
    num_cars = ctk.CTkEntry(master=input_grp, placeholder_text="Number of cars")
    num_stoplights = ctk.CTkEntry(master=input_grp, placeholder_text="Number of stoplights")

    def update_canvas():
        fractals = fractal_generator.generate_fractal().fractal_pixels
        print("Fractal generation done")
        
        colors = mapcolor(fractals, fractal_generator.max_iteration)
        img = Image.fromarray(colors, mode="RGB")
        
        canvas.image = ImageTk.PhotoImage(img)  
        canvas.create_image(450, 300, anchor="center", image=canvas.image) 
        x_label.configure(text=f"X = {fractal_generator.x:.2f}")
        i_label.configure(text=f"I = {fractal_generator.i:.2f}")

    def slider_event_x(event):
        value = slider_x.get()
        print(value)
        fractal_generator.set_x(value)
        update_canvas()

    def slider_event_i(event):
        value = slider_i.get()
        print(value)
        fractal_generator.set_i(value)
        update_canvas()
    

    def group_coordinates_by_proximity(coordinates, threshold):
        def distance(coord1, coord2):
            """Calculate Euclidean distance between two coordinates."""
            return ((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)**0.5

        groups = []
        for coord in coordinates:
            added = False
            for group in groups:
                if distance(coord, group['center']) <= threshold:
                    group['points'].append(coord)
                    group['center'] = (
                        sum(p[0] for p in group['points']) / len(group['points']),
                        sum(p[1] for p in group['points']) / len(group['points'])
                    )
                    added = True
                    break
            if not added:
                groups.append({'points': [coord], 'center': coord})

        # Extract the centers of each group
        return [group['center'] for group in groups]


    def start_city():
        coord_dict = fractal_generator.generate_pixel_coord_mapper()
        star_corods = coord_dict.get("*")
        underscore_coords = coord_dict.get("_")

        coordinates = star_corods + underscore_coords

        group_range_threshold = 80
        coordinates = group_coordinates_by_proximity(coordinates, group_range_threshold)

        print("COORDINATES: ", coordinates)

        segments, cars, stoplights = int(seg_len.get()), int(num_cars.get()), int(num_stoplights.get())
        root.destroy()
        city.init_city(
            1000,
            720, 
            segments,
            cars,
            stoplights,
            coordinates
        )

    # Update the canvas for the first time
    update_canvas()

    slider_grp.place(relx=0.70, rely=0.81, anchor="sw")
    input_grp.place(relx=0.10, rely=0.81, anchor="sw")
    
    x_label.place(relx=0.40, rely=0.2, anchor="sw")
    slider_x = ctk.CTkSlider(master=slider_grp, from_=-2, to=2)
    slider_x.set(fractal_generator.x)
    slider_x.place(relx=0.50, rely=0.3, anchor="center")
    slider_x.bind("<ButtonRelease-1>", slider_event_x)  # Bind slider release to event

    i_label.place(relx=0.40, rely=0.7, anchor="sw")
    slider_i = ctk.CTkSlider(master=slider_grp, from_=-2, to=2)
    slider_i.set(fractal_generator.i)
    slider_i.place(relx=0.50, rely=0.8, anchor="center")
    slider_i.bind("<ButtonRelease-1>", slider_event_i)  # Bind slider release to event
    
    seg_len.place(relx=0.5, rely=0.1, anchor="n")
    num_cars.place(relx=0.5, rely=0.4, anchor="n")
    num_stoplights.place(relx=0.5, rely=0.7, anchor="n")

    btn2 = ctk.CTkButton(master=frame, text="Start city simulation", command=start_city)
    btn2.place(relx=0.5, rely=0.9, anchor="s")
