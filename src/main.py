from tkinter import Tk, Label, ttk
from NotificationManager import NotificationManager
from PasswordManager import PasswordManager
from UI import UI
from UIStyle import UIStyle
from Login import Login

def start_manager(hash, derived_key):
    
    print("Starting Password Manager")
    print(f"Hash: {hash}")
    print(f"Derived Key: {derived_key}")
    
    window = Tk()
    window.title("Password Manager")
    window.iconbitmap("assets/icon.ico")
    window.resizable(False, False)
        
    ui_style = UIStyle(window)
    
    notification_label = Label(window, text="", width=40, font=ui_style.font, fg=ui_style.text_color, bg=ui_style.button_color)
    notification_label.grid(column=0, row=11, columnspan=3)
    
    notification_manager = NotificationManager(notification_label, ui_style)
    datafile = f"data/{hash}.json"
    password_manager = PasswordManager(notification_manager, datafile, derived_key)
    UI(window, password_manager, ui_style)

    window.mainloop()


if __name__ == "__main__":
     
    login_window = Tk()
    UIStyle(login_window)
    Login(login_window, start_manager)
    
    login_window.mainloop()
