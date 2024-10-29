from tkinter import Button, Label, Canvas, PhotoImage, Entry, END, Scale, Checkbutton, IntVar, ttk
from pyperclip import copy
import tkinter as tk


class UI:
    
    def __init__(self, window, password_manager, style):
        self.window = window
        self.password_manager = password_manager
        self.logo_img = PhotoImage(file="assets/logo.png")
        self.ui_style = style
        self.create_widgets()
        
    def create_button(self, root, text, command, width, row, column, sticky, columnspan):
        button = ttk.Button(root, text=text, style="Modern.TButton", command=command, width=width)
        button.grid(row=row, column=column, pady=10, sticky=sticky, columnspan=columnspan)
        return button
    
    def create_label(self, root, text, row, column, sticky, width, columnspan):
        label = ttk.Label(root, text=text, style="Modern.TLabel", width=width)
        label.grid(row=row, column=column, sticky=sticky, columnspan=columnspan)
        return label
    
    def create_entry(self, root, width, row, column, sticky, columnspan):
        entry = ttk.Entry(root, width=width, style="Modern.TEntry")
        entry.grid(row=row, column=column, sticky=sticky, columnspan=columnspan)
        return entry
    
    def create_checkbutton(self, root, text, variable, command):
        checkbutton = ttk.Checkbutton(root, text=text, variable=variable, command=command, style="Modern.TCheckbutton")
        return checkbutton

    def create_slider(self, root, from_, to, orient, length, command, showvalue):
        slider = tk.Scale(
            root,
            from_=from_,
            to=to,
            orient=orient,
            showvalue=showvalue,
            command=command,
            length=length,
            bg=self.ui_style.bg_color,            # Fondo del slider
            fg=self.ui_style.text_color,          # Color del texto del valor
            troughcolor= self.ui_style.entry_bg_color,       # Color de la ranura
            highlightbackground=self.ui_style.bg_color,  # Borde externo para que combine con el fondo
            activebackground=self.ui_style.button_hover_color   # Color del slider al hacer clic
        )
        return slider

    def create_widgets(self):
        self.window.title("Password Manager")
        self.window.config(padx=20, pady=20)
        self.window.minsize(width=480, height=420)

        canvas = Canvas(width=200, height=200, highlightthickness=0, bg=self.ui_style.bg_color)
        canvas.create_image(100, 100, image=self.logo_img)
        canvas.grid(column=0, row=0, columnspan=3)

        # Labels
        self.label_website = self.create_label(self.window, "Website:", 1, 0, "E", None, 1)
        
        self.label_username = self.create_label(self.window, "Email/Username:", 2, 0, "E", None, 1)
        
        self.label_password = self.create_label(self.window, "Password:", 3, 0, "E", None, 1)
        
        self.label_password_strength = self.create_label(self.window, "Strength:", 4, 0, "E", None, 1)
        self.label_password_strength.grid_forget()
        
        self.label_password_strength_value = self.create_label(self.window, "", 4, 1, "W", 25, 1)
        self.label_password_strength_value.grid_forget()
        
        self.label_password_length = self.create_label(self.window, "Length:", 5, 0, "E", None, 1)
        self.label_password_length.grid_forget()
        
        self.spacer = self.create_label(self.window, "", 10, 0, "W", None, 3)
        

        # Entries
        self.entry_website = self.create_entry(self.window, 30, 1, 1, "W", 1)
        self.entry_website.focus()

        self.entry_username = self.create_entry(self.window, 30, 2, 1, "W", 1)

        self.entry_password = self.create_entry(self.window, 30, 3, 1, "W", 1)

        # Buttons
        self.button_search = self.create_button(root=self.window, text="Search", command=self.search_password, width=20, row=1, column=2, sticky="W", columnspan=1)
        self.button_add = self.create_button(root=self.window, text="Add", command=self.save_password, width=60, row=11, column=0, sticky="W", columnspan=3)
        
        self.button_generate = self.create_button(root=self.window, text="Generate Password", command=self.generate_password, width=20, row=3, column=2, sticky="W", columnspan=1)

        self.toggle_button = self.create_button(root=self.window, text="More Options", command=self.toggle_options, width=20, row=4, column=2, sticky="W", columnspan=1)

        self.button_copy_username = self.create_button(root=self.window, text="Copy Username", command=self.copy_username, width=20, row=12, column=1, sticky="E", columnspan=1)
        self.button_copy_password = self.create_button(root=self.window, text="Copy Password", command=self.copy_password, width=20, row=12, column=2, sticky="W", columnspan=1)
        
        # Sliders
        self.slider_password_length = self.create_slider(self.window, from_=4, to=32, orient="horizontal", length=180, showvalue=16, command=self.on_slider_change)
        self.slider_password_length.set(16)

        # CheckButtons
        self.use_letters = IntVar(value=1)
        self.use_numbers = IntVar(value=1)
        self.use_symbols = IntVar(value=1)

        self.checkbutton_use_letters = self.create_checkbutton(self.window, "Use letters", self.use_letters, self.validate_checkbuttons)
        self.checkbutton_use_numbers = self.create_checkbutton(self.window, "Use numbers", self.use_numbers, self.validate_checkbuttons)
        self.checkbutton_use_symbols = self.create_checkbutton(self.window, "Use symbols", self.use_symbols, self.validate_checkbuttons)

        # Visibility
        self.options_visible = False

    def generate_password(self):
        max_length = self.slider_password_length.get()
        max_length = int(float(max_length))
        password = self.password_manager.generate_password(max_length, self.use_letters, self.use_numbers, self.use_symbols)
        self.entry_password.delete(0, END)
        self.entry_password.insert(0, password)

        # Copiar la contraseña al portapapeles
        self.password_manager.copy_password(password)

    def save_password(self):
        website = self.entry_website.get().strip()
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if self.password_manager.save_password(website, username, password):
            self.entry_website.delete(0, END)
            self.entry_password.delete(0, END)
            self.entry_username.delete(0, END)
            self.password_manager.notification_manager.show("Password saved successfully!", "green")

    def search_password(self):
        website = self.entry_website.get()
        data = self.password_manager.search_password(website)

        if data:
            self.entry_username.delete(0, END)
            self.entry_username.insert(0, data["email"])
            self.entry_password.delete(0, END)
            self.entry_password.insert(0, data["password"])
            self.password_manager.copy_password(data["password"])
        else:
            self.password_manager.notification_manager.show("No details for the website exist!", "red")

    def validate_checkbuttons(self):
        selected_options = sum([self.use_letters.get(), self.use_numbers.get(), self.use_symbols.get()])
        if selected_options == 1:
            if self.use_letters.get() == 1:
                self.checkbutton_use_letters.config(state="disabled")
            elif self.use_numbers.get() == 1:
                self.checkbutton_use_numbers.config(state="disabled")
            elif self.use_symbols.get() == 1:
                self.checkbutton_use_symbols.config(state="disabled")
        else:
            self.checkbutton_use_letters.config(state="normal")
            self.checkbutton_use_numbers.config(state="normal")
            self.checkbutton_use_symbols.config(state="normal")

    def toggle_options(self):
        self.options_visible = not self.options_visible
        if self.options_visible:
            self.toggle_button.config(text="Less Options")
            self.checkbutton_use_letters.grid(column=1, row=7, sticky="W")
            self.checkbutton_use_numbers.grid(column=1, row=8, sticky="W")
            self.checkbutton_use_symbols.grid(column=1, row=9, sticky="W")
            self.label_password_length.grid(column=0, row=5, sticky="E")
            self.slider_password_length.grid(column=1, row=5, sticky="W")
            self.label_password_strength.grid(column=0, row=4, sticky="E")
            self.label_password_strength_value.grid(column=1, row=4)
        else:
            self.toggle_button.config(text="More Options")
            self.checkbutton_use_letters.grid_forget()
            self.checkbutton_use_numbers.grid_forget()
            self.checkbutton_use_symbols.grid_forget()
            self.label_password_length.grid_forget()
            self.slider_password_length.grid_forget()
            self.label_password_strength.grid_forget()
            self.label_password_strength_value.grid_forget()
            
            
            
    def on_slider_change(self, value):
        strenght = ["Weak", "Medium", "Strong", "Very Strong"]
        strenght_colors = ["red", "orange", "green", "light blue"]
        
        value = int(value)
        
        if value <= 6:
            self.label_password_strength_value.config(text=strenght[0], foreground="white", font=("Arial", 10, "bold"), background=strenght_colors[0])
        elif value <= 10:
            self.label_password_strength_value.config(text=strenght[1], foreground="white", font=("Arial", 10, "bold"), background=strenght_colors[1])
        elif value < 16:
            self.label_password_strength_value.config(text=strenght[2], foreground="white", font=("Arial", 10, "bold"), background=strenght_colors[2])
        else:
            self.label_password_strength_value.config(text=strenght[3], foreground="white", font=("Arial", 10, "bold"), background=strenght_colors[3])
            
    def copy_to_clipboard(self, content, content_type):
        if content == "":
            self.password_manager.notification_manager.show(f"No {content_type} to copy!", "red")
            return
        self.password_manager.notification_manager.show(f"{content_type.capitalize()} copied to clipboard!", "green")
        copy(content)

    def copy_username(self):
        username = self.entry_username.get()
        self.copy_to_clipboard(username, "username")

    def copy_password(self):
        password = self.entry_password.get()
        self.copy_to_clipboard(password, "password")
