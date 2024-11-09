from random import choice, shuffle
from pyperclip import copy
from tkinter import messagebox
from CryptoManager import CryptoManager

class PasswordManager:
    def __init__(self, notification_manager, datafile, key):
        self.notification_manager = notification_manager
        self.letters = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)]
        self.numbers = [str(i) for i in range(10)]
        self.symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
        self.datafile = datafile
        self.crypto_manager = CryptoManager()
        self.key = key
        
        # print("Password Manager initialized")
        # print(f"Datafile: {self.datafile}")
        # print(f"Key: {self.key}")
        

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
            self.notification_manager.show("Por favor llenar todos los campos!", "red")
            return

        is_ok = messagebox.askokcancel(title=website, message=f"Son estos datos correctos?\nUsuario: {username}\nContraseña: {password}\n")

        if is_ok:
            new_data = {website: {"email": username, "password": password}}
            if self.save_password_data(new_data):
                return True
        
        return False

    def save_password_data(self, new_data):
        try:
            data = self.crypto_manager.decrypt_file(self.datafile, self.key)
        except FileNotFoundError:
            data = {}
        
        #verificar si los datos ya existen
        for key in new_data:
            print(f"Key: {key}")
            if key in data:
                self.notification_manager.show(f"El sitio {key} ya existe!", "red")
                print(f"El sitio {key} ya existe!")
                return False
        
        data.update(new_data)
        self.crypto_manager.encrypt_file(self.datafile, data, self.key)
        return True
                
    def modify_password(self, website, username, password):
        new_data = {website: {"email": username, "password": password}}
        try:
            data = self.crypto_manager.decrypt_file(self.datafile, self.key)
        except FileNotFoundError:
            return False
        
        data.update(new_data)
        self.crypto_manager.encrypt_file(self.datafile, data, self.key)
        return True

        
    def delete_password(self, website):
        try:
            data = self.crypto_manager.decrypt_file(self.datafile, self.key)
            data.pop(website)
            self.crypto_manager.encrypt_file(self.datafile, data, self.key)
        except Exception as e:
            return e
        else:
            return None

    def search_password(self, website):
        try:
            data = self.crypto_manager.decrypt_file(self.datafile, self.key)
        except FileNotFoundError:
            self.notification_manager.show("Archivo no encontrado!", "red")
            return None
        else:
            return data.get(website)

    def copy_password(self, password):
        copy(password)
        self.notification_manager.show("Contraseña copiada!", "green")

    def get_all_sites(self):
        try:
            data = self.crypto_manager.decrypt_file(self.datafile, self.key)
            # Devuelve una lista de los sitios (claves) en los datos
            return list(data.keys())
        except FileNotFoundError:
            self.notification_manager.show("Archivo no encontrado!", "red")
            return []
        except Exception as e:
            self.notification_manager.show(f"Error: {e}", "red")
            return []