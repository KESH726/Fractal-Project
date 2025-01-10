import customtkinter as ctk
from CTkTable import *
import os

import tkinter as tk
# from . import render_page


def leaderboards(root,frame):
     root_dir = os.curdir
     data_dir = os.path.join(root_dir, "data")

     file = open(os.path.join(data_dir, "savedata.txt"), "r")
     file_content = []
     file_content_header = [["Rank","City Name","Score"]]

     for idx, line in enumerate(file.read().splitlines()):
          temp_arr = ["#"+str(idx)]
          temp_arr = temp_arr + line.split(" ")
          file_content.append(temp_arr)
          

     file_content.sort(key=lambda x: int(x[2]), reverse=True)
     file_content = file_content_header + file_content

     leaderboard_image = tk.PhotoImage(file="src/assets/leaderboard.png")
     label = ctk.CTkLabel(master = frame, image = leaderboard_image )
     label.pack(expand=True, fill="both", padx=4, pady=4)

     scrollbar = ctk.CTkScrollbar(master=frame, orientation="vertical", height=400, width=20,corner_radius=0)

     table = CTkTable(master=scrollbar, column=3, values=file_content, hover_color = "#696665")
     table.pack(expand=True, fill="both", padx=20, pady=20)
     scrollbar.pack(expand=True, fill="both", padx=20, pady=20)

