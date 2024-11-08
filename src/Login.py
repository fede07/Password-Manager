import tkinter as tk
from tkinter import Canvas
from os import listdir, makedirs
from os.path import exists
from CryptoManager import CryptoManager
from UICreator import UICreator

class Login:
    
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.hash = None
        self.derived_key = None
        
        # Configuración de la ventana principal
        self.root.title("Password Manager Login")
        self.root.geometry("400x480")
        self.root.resizable(False, False)

        # Configura las columnas y filas de la raíz para expandirse
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        
        # Logo
        canvas = Canvas(self.root, width=200, height=200, highlightthickness=0, bg="#F7F8FA")
        self.logo_image = tk.PhotoImage(file="assets/logo.png")
        canvas.create_image(100, 100, image=self.logo_image)
        canvas.grid(column=1, row=0, columnspan=2, sticky="n", pady=(20, 10))
        
        # Etiquetas y campos de entrada
        self.username_label = UICreator.create_label(self.root, "Usuario:", row=1, column=1, sticky="e", width=10, columnspan=1)
        self.username_entry = UICreator.create_entry(self.root, width=20, row=1, column=2, sticky="w", columnspan=1)
        self.username_entry.focus()
        
        self.password_label = UICreator.create_label(self.root, "Contraseña:", row=2, column=1, sticky="e", width=10, columnspan=1)
        self.password_entry = UICreator.create_entry(self.root, width=20, row=2, column=2, sticky="w", columnspan=1)
        self.password_entry.config(show="*")
        
        self.notification_label = UICreator.create_label(self.root, "", row=13, column=1, sticky="n", width=30, columnspan=2)
        
        # Botones
        self.login_button = UICreator.create_button(self.root, "Login", self.login, width=15, row=4, column=1, columnspan=2, sticky="n")
        self.register_button = UICreator.create_button(self.root, "Registrar", self.register, width=15, row=5, column=1, columnspan=2, sticky="n")
    
        # Checkbox para mostrar la contraseña
        
        self.show_password = tk.IntVar()
        self.show_password_checkbutton = UICreator.create_checkbutton(self.root, "Mostrar contraseña", self.show_password, self.toggle_password)
        self.show_password_checkbutton.grid(row=3, column=2, sticky="n")
    
        # Configuración de los botones
    
        self.login_button.grid_configure(pady=10)
        self.register_button.grid_configure(pady=5)
        
        self.root.grid_rowconfigure(1, pad=10)  # Espacio para la fila del username
        self.root.grid_rowconfigure(2, pad=10)  # Espacio para la fila del password

                        
    def login(self):
        
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.check_empty_fields(username, password):
            return
        
        if self.verify_credentials(username, password):
            self.root.destroy()
            self.on_success(self.hash, self.derived_key)
        else:
            self.show("Credenciales incorrectas", "red")

    def check_empty_fields(self, username, password):
        if len(username) == 0 or len(password) == 0:
            self.show("Por favor llenar todos los campos", "red")
            return True
        return False
            
    def verify_credentials(self, username, password):
        
        data_folder = "data"
        
        self.hash = CryptoManager.generate_hash(username)
        self.derived_key = CryptoManager.derive_key(password, username)
        
        if not self.verify_existing_user(username):
            return False
        
        if CryptoManager.decrypt_file(f"{data_folder}/{self.hash}.json", self.derived_key) is None:
            return False
            
        return True
    
    def verify_existing_user(self, username):
        data_folder = "data"
        hash = CryptoManager.generate_hash(username)
        return hash + ".json" in listdir(data_folder)
    
    
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.check_empty_fields(username, password):
            return
        
        exists_user = self.verify_existing_user(username)        
        
        if exists_user:
            self.show("Usuario ya registrado", "red")
            return
        
        self.hash = CryptoManager.generate_hash(username)
        self.derived_key = CryptoManager.derive_key(password, username)
        filename = "data/" + self.hash + ".json"
        if not exists("data"):
            makedirs("data")
        CryptoManager.encrypt_file(filename, {}, self.derived_key)
        CryptoManager.encrypt_file(filename, {}, self.derived_key)
        
        self.show("Usuario registrado correctamente!", "green")
        
    def show(self, message, color):
        self.notification_label.config(text=message, foreground=color)
        self.notification_label.grid(column=1, row=6, columnspan=2, sticky="n")
        
    def toggle_password(self):
        if self.password_entry.cget("show") == "":
            self.password_entry.config(show="*")
        else:
            self.password_entry.config(show="")