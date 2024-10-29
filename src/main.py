from tkinter import Tk, Label
from NotificationManager import NotificationManager
from PasswordManager import PasswordManager
from UI import UI

if __name__ == "__main__":
    window = Tk()
    window.title("Password Manager")
    window.resizable(False, False)
    notification_label = Label(window, text="", width=40)
    notification_label.grid(column=0, row=11, columnspan=3)

    notification_manager = NotificationManager(notification_label)
    password_manager = PasswordManager(notification_manager)
    ui = UI(window, password_manager)

    window.mainloop()
