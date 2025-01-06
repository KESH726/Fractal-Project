import customtkinter as ctk
from CTkTable import *

import tkinter as tk
# from . import render_page


def leaderboards(root,frame):
    value = [
        ["Rank","City Name","Score"],
             [
        "#1","City 1",3,],
             ["#2","City 2",6,],
             ["#3","City 3",10,],
             ["#4","City 4",12,],
             ["#5","City 5",14,],
             ["#6","City 6",15,],
             ["#7","City 7",20,],
             ["#7","City 7",20,],
             ["#7","City 7",20,],
             ["#7","City 7",20,],
             ["#7","City 7",20,],
             ["#7","City 7",20,],
             ["#7","City 7",20,],
             
         ]
    
    leaderboard_image = tk.PhotoImage(file="src/pages/leaderboard_png.png")
    label = ctk.CTkLabel(master = frame, image = leaderboard_image )
    label.pack(expand=True, fill="both", padx=4, pady=4)

    scrollbar = ctk.CTkScrollbar(master=frame, orientation="vertical", height=400, width=20,corner_radius=0)

    table = CTkTable(master=scrollbar, column=3, values=value, hover_color = "#696665")
    table.pack(expand=True, fill="both", padx=20, pady=20)
    scrollbar.pack(expand=True, fill="both", padx=20, pady=20)
    
    