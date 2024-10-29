from tkinter import Tk, Label, ttk
from NotificationManager import NotificationManager
from PasswordManager import PasswordManager
from UI import UI
from UIStyle import UIStyle

if __name__ == "__main__":
    window = Tk()
    window.title("Password Manager")
    window.iconbitmap("assets/icon.ico")
    window.resizable(False, False)
    ui_style = UIStyle(window)
    
    notification_label = Label(window, text="", width=40, font=ui_style.font, fg=ui_style.text_color, bg=ui_style.button_color)
    notification_label.grid(column=0, row=11, columnspan=3)
    
    
    notification_manager = NotificationManager(notification_label, ui_style)
    password_manager = PasswordManager(notification_manager)
    ui = UI(window, password_manager, ui_style)

    window.mainloop()
