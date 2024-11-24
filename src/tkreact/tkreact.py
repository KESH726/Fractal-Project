from typing import Callable
import customtkinter as ctk

# Manages your tkinter app's "root" in the background
class RootManager:
    _root = None  # Internal variable for the root reference
    _current_frame = None  # Internal variable that references the current frame

    @staticmethod
    def set_root(root):
        RootManager._root = root
    
    @staticmethod
    def set_frame(frame):
        RootManager._current_frame = frame

    @staticmethod
    def get_root():
        if RootManager._root is None:
            raise ValueError("Root has not been set!")
        return RootManager._root

    @staticmethod
    def get_frame(frame):
        if RootManager._current_frame is None:
            raise ValueError("Current frame has not been set!")
        return RootManager._current_frame

    @staticmethod
    def clear_screen():
        root = RootManager.get_root()
        for widget in root.winfo_children():
            widget.destroy()

    @staticmethod
    def create_frame(**kwargs):
        RootManager.clear_screen()
        root = RootManager.get_root()
        frame = ctk.CTkFrame(master=root, **kwargs)
        frame.pack(pady=20, padx=60, fill="both", expand=True)
        RootManager.set_frame(frame)
        return frame


# Global state manager of your application
class Context:
    # Store global state in a dictionary
    _global_state = {}

    @staticmethod
    def set_var(key, value):
        """Sets a value for a given key in the global state."""
        Context._global_state[key] = value

    @staticmethod
    def get_var(key):
        """Gets the value of a given key from the global state."""
        if key in Context._global_state:
            return Context._global_state[key]
        else:
            raise KeyError(f"{key} not found in global state")

    @staticmethod
    def remove_var(key):
        """Removes a key from the global state."""
        if key in Context._global_state:
            del Context._global_state[key]
        else:
            raise KeyError(f"{key} not found in global state")


# Initialise tkinter app & render first page
def create_app(title, window_size, appearance, theme, homepage):
    ctk.set_appearance_mode(appearance)
    ctk.set_default_color_theme(theme)
    
    root = ctk.CTk()
    RootManager.set_root(root)

    root.geometry(window_size)
    name = root.title(title)

    render_page(homepage)

    root.mainloop()


# Renders a new page by clearing screen & creating a new frame
def render_page(page: Callable[[ctk.CTk, ctk.CTkFrame], None]):
    RootManager.clear_screen()
    root = RootManager.get_root()
    frame = RootManager.create_frame()
    page(root, frame)


# Renders a specific component (without clearing the page)
# props can be passed to component as args or a dictionary
def use_component(component: Callable[[ctk.CTk, ctk.CTkFrame], None], *args, **kwargs):
    root = RootManager.get_root()
    frame = RootManager.get_frame()
    component(root, frame, *args, **kwargs)