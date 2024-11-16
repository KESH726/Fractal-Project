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


#need to create an environment for the recursion
def click_window():
    new_window = ctk.CTk()
    new_window.geometry("960x600")
    name2 = new_window.title("test")
    
    frame_2 = ctk.CTkFrame(master=new_window)
    frame_2.pack(pady=20, padx=60, fill="both", expand = True)
    
    root.destroy()

    label = ctk.CTkLabel(master = new_window, text = "adjust how big the graph is", font = ("Aerial", 20))
    label.place(relx = 0.1, rely = 0.85, anchor = "sw")
    
    
    def slider(value):
        print(value)
    slider_1 = ctk.CTkSlider(master = new_window, from_=0, to=100, command = slider)
    slider_1.place(relx = 0.1, rely = 0.9, anchor = "sw")
    
    
    new_window.mainloop()
    

btn1 = ctk.CTkButton(master=frame, text = "Start", command=click_window)
btn1.place(relx=0.5, rely=0.5, anchor="center")


#the switch for toggling on and off light and dark mode
def switch():
    ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

switch_var = ctk.StringVar(value="on")
switch = ctk.CTkSwitch(root, text="CTkSwitch", command=switch, variable=switch_var, onvalue="on", offvalue="off")
switch.place(relx = 0.07 , rely = 0.05, anchor = "nw")


#quit button
def quit():
    root.destroy()

btn2 = ctk.CTkButton(master=frame, text = "Quit", command = quit)
btn2.place(relx=0.5, rely=0.7, anchor="s")








# label = ctk.CTkLabel(master = frame, text = "login System")
# label.pack(pady = 12, padx= 10)

# entry1 = ctk.CTkEntry(master = frame, placeholder_text="Username")
# entry1.pack(pady =12, padx= 10)

# entry2 = ctk.CTkEntry(master = frame, placeholder_text="Password", show="*")
# entry2.pack(pady =12, padx= 10)

# button = ctk.CTkButton(master = frame, text="login", command=login)
# button.pack(pady=12, padx=10)

# checkbox = ctk.CTkCheckBox(master=frame, text="Remember me")
# checkbox.pack(pady=12, padx=10)

root.mainloop()