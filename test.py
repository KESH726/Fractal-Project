from tkinter import *
import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.geometry("960x600")
name = root.title("Recursive graphics project")

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand = True)

label = ctk.CTkLabel(master=frame, text = "Ready to start the game?", font = ("Aerial", 20))
label.place(relx=0.5, rely=0.3, anchor = "n")


#creates another empty window 
def click_window():
    new_window = ctk.CTk()
    new_window.geometry("960x600")
    name2 = new_window.title("test")
    
    frame_2 = ctk.CTkFrame(master=new_window)
    frame_2.pack(pady=20, padx=60, fill="both", expand = True)
    
    root.destroy() #destroys old window(root)

    label = ctk.CTkLabel(master = new_window, text = "adjust how big the graph is", font = ("Aerial", 20))
    label.place(relx = 0.1, rely = 0.85, anchor = "sw")
    
    
    def slider(value):
        print(value)
    slider_1 = ctk.CTkSlider(master = new_window, from_=0, to=100, command = slider)
    slider_1.place(relx = 0.1, rely = 0.9, anchor = "sw")
    
    
    new_window.mainloop()
    

btn1 = ctk.CTkButton(master=frame, text = "Start", command=click_window)
btn1.place(relx=0.5, rely=0.5, anchor="center")


#quit button
def quit():
    root.destroy()

btn2 = ctk.CTkButton(master=frame, text = "Quit", command = quit)
btn2.place(relx=0.5, rely=0.7, anchor="s")


root.mainloop()