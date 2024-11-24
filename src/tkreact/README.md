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

---

### Create app
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

---

### Pages
Pages in tkreact are just functions that look like this:
* 1 - Logic first
* 2 - UI after
Note: pages must always have root & frame as a parameter
```python
import customtkinter as ctk

def main_menu(root, frame):
    def quit_button():
        root.destroy()
    
    btn2 = ctk.CTkButton(master=frame, text="Quit", command=quit_button)
    btn2.place(relx=0.5, rely=0.7, anchor="s")
``` 

To navigate to a different page, simply use the function `render_page()`
```python
render_page(my_page)
```

---

### Components
Components are reusable UI elements
E.g. if you made a custom button, you can reuse it as much as you'd like

And they are defined in the same way as pages, but 
they have one extra feature: props

Props are variables that you can pass to a component
```python
# Component definition for a button
def MyButton(root, frame, label_text, width, height):
    button = ctk.CTkButton(master=frame, text=label_text, width=width, height=height)
    button.pack()

# Component usage
use_component(MyButton, label_text="Start Game", width=200, height=60)
```

---

### Context – Managing Global State

`Context` is a class used for managing global state that can be accessed anywhere in your app.

You can set and get variables using the static methods `Context.set_var()` and `Context.get_var()`.

```python
# Setting a global variable
Context.set_var("score", 0)

# Getting a global variable
score = Context.get_var("score")
print(score)  # Output: 0
```

Here's Context being used with a component:
```python
# Component definition using Context
def ScoreLabel(root, frame):
    score = Context.get_var("score")  # Accessing global state
    label = ctk.CTkLabel(master=frame, text=f"Score: {score}", font=("Arial", 16))
    label.pack()

# Usage of ScoreLabel component
use_component(ScoreLabel)
```
