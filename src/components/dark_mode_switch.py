from src.tkreact import Context
import customtkinter as ctk
   
# Dark Mode Switch Component
def dark_mode_switch(root, frame):
    def toggle_theme():
        Context.set_var("dark", not (Context.get_var("dark")))

        match Context.get_var("dark"):
            case True:
                ctk.set_appearance_mode("dark")
            case False:
                ctk.set_appearance_mode("light")
            case _:
                print("wtf")
    
    def get_current_theme_state():
        return Context.get_var("dark")    

    # Put the UI of the button here
    btn_darkmode = ctk.CTkButton(frame, text = 'Dark/Light', command = toggle_theme)
    btn_darkmode.pack(pady = 10)
