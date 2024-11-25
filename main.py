from tkinter import *
import tkinter as tk
import customtkinter as ctk
import pygame

from src.tkreact import create_app
from src.pages import main_menu

# Initialise tkinter & run app
create_app(
    title="Recursive graphics project",
    window_size="960x600",
    appearance="dark",
    theme="dark-blue",
    homepage=main_menu
)