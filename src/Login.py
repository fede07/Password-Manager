import tkinter as tk
from tkinter import messagebox, Canvas
from os import listdir
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
        self.root.geometry("400x450")
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
        
        self.password_label = UICreator.create_label(self.root, "Contraseña:", row=2, column=1, sticky="e", width=10, columnspan=1)
        self.password_entry = UICreator.create_entry(self.root, width=20, row=2, column=2, sticky="w", columnspan=1)
        
        # Botones
        self.login_button = UICreator.create_button(self.root, "Login", self.login, width=15, row=3, column=1, columnspan=2, sticky="n")
        self.register_button = UICreator.create_button(self.root, "Registrar", self.register, width=15, row=4, column=1, columnspan=2, sticky="n")
    
    
        self.login_button.grid_configure(pady=10)
        self.register_button.grid_configure(pady=5)
        
        self.root.grid_rowconfigure(1, pad=10)  # Espacio para la fila del username
        self.root.grid_rowconfigure(2, pad=10)  # Espacio para la fila del password



                        
    def login(self):
        
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        #TESTING
        # print("-----------------TESTING HABILITADO-----------------")
        # username = "TestUser"
        # password = "1234"
        
        self.derived_key = CryptoManager.derive_key(password, username)
        self.hash = CryptoManager.generate_hash(username, password)
        
        if self.verify_credentials(username, password):
            self.root.destroy()
            self.on_success(self.hash, self.derived_key)
            #Iniciar la aplicación principal
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            
    def verify_credentials(self, username, password):
        
        data_folder = "data"
        
        self.hash = CryptoManager.generate_hash(username, password)
        if self.hash + ".json" not in listdir(data_folder):
            return False
        return True
    
    
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if len(username) == 0 or len(password) == 0:
            messagebox.showerror("Error", "Por favor, rellena todos los campos")
            return
        
        if self.verify_credentials(username, password):
            messagebox.showerror("Error", "El usuario ya existe")
            return
        
        self.hash = CryptoManager.generate_hash(username, password)
        self.derived_key = CryptoManager.derive_key(password, username)
        filename = "data/" + self.hash + ".json"
        
        CryptoManager.encrypt_file(filename, {}, self.derived_key)
        
        messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        
        