import customtkinter as ctk
from src.tkreact import render_page, use_component

# Components
from src.components import dark_mode_switch

# Pages
from .fractal_editor import fractal_editor
from .leaderboards import leaderboards

def main_menu(root, frame):
    # Logic
    def start_button():
        render_page(fractal_editor)

    def quit_button():
        root.destroy()
        
    def start_leaderboard_page():
        render_page(leaderboards)
    
    # UI
    label = ctk.CTkLabel(master=frame, text="Fractal Road Network", font = ("Aerial", 20))
    label.place(relx=0.5, rely=0.3, anchor = "n")
    
    btn1 = ctk.CTkButton(master=frame, text="Create a fractal", command=start_button)
    btn1.place(relx=0.5, rely=0.5, anchor="center")
    btn1 = ctk.CTkButton(master=frame, text="See the leader board", command=start_leaderboard_page)
    btn1.place(relx=0.5, rely=0.7, anchor="center")
    
    btn2 = ctk.CTkButton(master=frame, text="Quit", command=quit_button)
    btn2.place(relx=0.5, rely=0.9, anchor="s")

    # Dark mode switch component
    use_component(dark_mode_switch)
    
