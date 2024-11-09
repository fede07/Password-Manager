from tkinter import Tk
from PasswordManager import PasswordManager
from UI import UI
from UIStyle import UIStyle
from Login import Login

WIDTH = 600
HEIGHT = 600

def start_manager(hash, derived_key):
    
    window = Tk()
    window.title("Password Manager")
    window.iconbitmap("assets/icon.ico")
    window.resizable(False, False)
        
    ui_style = UIStyle(window)

    datafile = f"data/{hash}.json"
    password_manager = PasswordManager(datafile= datafile, key= derived_key, notification_manager=None)
    UI(window, password_manager, ui_style)

    window.mainloop()


if __name__ == "__main__":
     
    login_window = Tk()
    UIStyle(login_window)
    Login(login_window, start_manager)
    
    login_window.iconbitmap("assets/icon.ico")
    
    login_window.mainloop()
