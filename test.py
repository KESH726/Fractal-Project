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
    pygame.init()
    
    root.destroy() #destroys old window(root)
    
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    run = True
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
pygame.quit()
    

btn1 = ctk.CTkButton(master=frame, text = "Start", command=click_window)
btn1.place(relx=0.5, rely=0.5, anchor="center")


#quit button
def quit():
    root.destroy()

btn2 = ctk.CTkButton(master=frame, text = "Quit", command = quit)
btn2.place(relx=0.5, rely=0.7, anchor="s")


root.mainloop()
