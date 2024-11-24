# tkreact tutorial

Small library that I decided to write to abstract away some tkinter stuff.

Features
* Page transitions
* Components (with props)
* Global state

How to use:
* create_app - takes 5 arguments: title, window size, appearance mode, theme, homepage
* render_page - takes 1 argument: page name
* use_component - takes 2+ arguments: component name, props

* Context.set_var() - takes 2 arguments: key, value
* Context.get_var() - takes 1 argument: key
* Context.remove_var() - takes 1 argument: key

## Example
Here's a simple example of how to initialise a tkreact app
We have configured some settings like the name and theme.
And we have set the homepage to "main_menu" which is a tkreact "page"

```python
import customtkinter as ctk
from src.tkreact import create_app
from src.pages import main_menu

create_app(
    title="My Tkinter App",
    window_size="800x600",
    appearance="dark",
    theme="blue",
    homepage=main_menu
)
```

Pages in tkreact are just functions that look like this:
1 - Logic first
2 - UI after
Note: pages must always have root & frame as a parameter
```python
import customtkinter as ctk

def main_menu(root, frame):
    def quit_button():
        root.destroy()
    
    btn2 = ctk.CTkButton(master=frame, text="Quit", command=quit_button)
    btn2.place(relx=0.5, rely=0.7, anchor="s")
``` 