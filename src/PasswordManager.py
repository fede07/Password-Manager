from random import choice, shuffle
from pyperclip import copy
from tkinter import messagebox
import json

class PasswordManager:
    def __init__(self, notification_manager):
        self.notification_manager = notification_manager
        self.letters = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)]
        self.numbers = [str(i) for i in range(10)]
        self.symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
        self.datafile = "data/data.json"

    def generate_password(self, max_length, use_letters, use_numbers, use_symbols):
        password_list = []

        # Asegurarse de incluir al menos un carácter de cada tipo seleccionado
        if use_letters.get() == 1:
            password_list.append(choice(self.letters))
        if use_numbers.get() == 1:
            password_list.append(choice(self.numbers))
        if use_symbols.get() == 1:
            password_list.append(choice(self.symbols))

        # Completar el resto de la contraseña con caracteres aleatorios según las opciones seleccionadas
        while len(password_list) < max_length:
            if use_letters.get() == 1:
                password_list.append(choice(self.letters))
            if use_numbers.get() == 1:
                password_list.append(choice(self.numbers))
            if use_symbols.get() == 1:
                password_list.append(choice(self.symbols))

        # Limitar el tamaño total a max_length y mezclar los caracteres
        password_list = password_list[:max_length]
        shuffle(password_list)
        return ''.join(password_list)

    def save_password(self, website, username, password):
        if len(website) == 0 or len(username) == 0 or len(password) == 0:
            self.notification_manager.show("Please fill in all the fields!", "red")
            return

        is_ok = messagebox.askokcancel(title=website, message=f"Are these details correct?\nUsername: {username}\nPassword: {password}\n")

        if is_ok:
            new_data = {website: {"email": username, "password": password}}
            try:
                with open(file=self.datafile, mode="r") as saved_data:
                    data = json.load(saved_data)
                    data.update(new_data)
            except FileNotFoundError:
                with open(file=self.datafile, mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                with open(file=self.datafile, mode="w") as data_file:
                    json.dump(data, data_file, indent=4)

            return True
        return False

    def search_password(self, website):
        try:
            with open(file=self.datafile, mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            self.notification_manager.show("No Data File Found!", "red")
            return None
        else:
            return data.get(website)

    def copy_password(self, password):
        copy(password)
        self.notification_manager.show("Password copied to clipboard!", "green")
