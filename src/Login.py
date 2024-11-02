import tkinter as tk
from tkinter import messagebox, ttk
from os import listdir
from CryptoManager import CryptoManager
class Login:
    
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.hash = None
        self.derived_key = None
        
        self.root.title("Password Manager Login")
        self.root.geometry("300x300")
                
        self.username_label = ttk.Label(self.root, text="Usuario:")
        self.username_label.grid(column=0, row=0)
        self.username_entry = ttk.Entry(self.root)
        self.username_entry.grid(column=1, row=0)
        
        self.password_label = ttk.Label(self.root, text="Contraseña:")
        self.password_label.grid(column=0, row=1)
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.grid(column=1, row=1)
        
        self.login_button = ttk.Button(self.root, text="Login", command=self.login)
        self.login_button.grid(column=0, row=2, columnspan=2)
        
        self.register_button = ttk.Button(self.root, text="Registrar", command=self.register)
        self.register_button.grid(column=0, row=3, columnspan=2)
                        
    def login(self):
        
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        #TESTING
        print("-----------------TESTING HABILITADO-----------------")
        username = "TestUser"
        password = "1234"
        
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
        
        