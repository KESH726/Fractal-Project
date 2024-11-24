import customtkinter as ctk
import pygame

def fractal_editor(root, frame):
    def start_simulation():
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

    label = ctk.CTkLabel(master=frame, text="Fractal Editor", font = ("Aerial", 20))
    label.place(relx=0.5, rely=0.3, anchor = "n")

    btn1 = ctk.CTkButton(master=frame, text="Start city simulation", command=start_simulation)
    btn1.place(relx=0.5, rely=0.5, anchor="center")