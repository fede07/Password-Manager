from tkinter import Canvas, PhotoImage, END, Scale, IntVar
from pyperclip import copy
from UICreator import UICreator

class UI:
    
    def __init__(self, window, password_manager, style):
        self.window = window
        self.password_manager = password_manager
        self.logo_img = PhotoImage(file="assets/logo.png")
        self.ui_style = style
        self.create_widgets()
        
    def create_slider(self, root, from_, to, orient, length, command, showvalue):
        slider = Scale(
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
        self.label_website = UICreator.create_label(self.window, "Sitio:", 1, 0, "E", None, 1)
        
        self.label_username = UICreator.create_label(self.window, "Email/Usuario:", 2, 0, "E", None, 1)
        
        self.label_password = UICreator.create_label(self.window, "Contraseña:", 3, 0, "E", None, 1)
        
        self.label_password_strength = UICreator.create_label(self.window, "Fuerza:", 4, 0, "E", None, 1)
        self.label_password_strength.grid_forget()
        
        self.label_password_strength_value = UICreator.create_label(self.window, "", 4, 1, "W", 25, 1)
        self.label_password_strength_value.grid_forget()
        
        self.label_password_length = UICreator.create_label(self.window, "Largo:", 5, 0, "E", None, 1)
        self.label_password_length.grid_forget()
        
        self.spacer = UICreator.create_label(self.window, "", 10, 0, "W", None, 3)
        
        # Dropdown to show saved sites
        self.dropdown_sites = UICreator.create_combobox(self.window, values=[], width=28, row=1, column=1, sticky="W", columnspan=1)
        self.dropdown_sites.bind("<<ComboboxSelected>>", self.populate_from_dropdown)
        self.dropdown_sites.focus()

        self.entry_username = UICreator.create_entry(self.window, 30, 2, 1, "W", 1)

        self.entry_password = UICreator.create_entry(self.window, 30, 3, 1, "W", 1)

        # Buttons
        # self.button_search = UICreator.create_button(root=self.window, text="Search", command=self.search_password, width=20, row=1, column=2, sticky="W", columnspan=1)
        self.button_add = UICreator.create_button(root=self.window, text="Agregar contraseña", command=self.save_password, width=60, row=11, column=0, sticky="W", columnspan=3)
        
        self.button_generate = UICreator.create_button(root=self.window, text="Generar contraseña", command=self.generate_password, width=20, row=4, column=1, sticky="W", columnspan=1)

        self.toggle_button = UICreator.create_button(root=self.window, text="Más Opciones", command=self.toggle_options, width=20, row=4, column=2, sticky="W", columnspan=1)

        self.button_copy_username = UICreator.create_button(root=self.window, text="Copiar usuario", command=self.copy_username, width=20, row=2, column=2, sticky="W", columnspan=1)
        self.button_copy_password = UICreator.create_button(root=self.window, text="Copiar contraseña", command=self.copy_password, width=20, row=3, column=2, sticky="W", columnspan=1)
        
        # Sliders
        self.slider_password_length = self.create_slider(self.window, from_=4, to=32, orient="horizontal", length=180, showvalue=16, command=self.on_slider_change)
        self.slider_password_length.set(16)

        # CheckButtons
        self.use_letters = IntVar(value=1)
        self.use_numbers = IntVar(value=1)
        self.use_symbols = IntVar(value=1)

        self.checkbutton_use_letters = UICreator.create_checkbutton(self.window, "Usar letras", self.use_letters, self.validate_checkbuttons)
        self.checkbutton_use_numbers = UICreator.create_checkbutton(self.window, "Usar numeros", self.use_numbers, self.validate_checkbuttons)
        self.checkbutton_use_symbols = UICreator.create_checkbutton(self.window, "Usar simbolos", self.use_symbols, self.validate_checkbuttons)

        # Visibility
        self.options_visible = False
        
        self.load_sites()
    
    def load_sites(self):
        sites = self.password_manager.get_all_sites()
        self.dropdown_sites['values'] = sites if sites else ["No hay sitios guardados"]
        
    def populate_from_dropdown(self, event):
        """Populate username and password fields based on dropdown selection."""
        selected_site = self.dropdown_sites.get()
        if selected_site:
            data = self.password_manager.search_password(selected_site)
            if data:
                self.entry_username.delete(0, END)
                self.entry_username.insert(0, data["email"])
                self.entry_password.delete(0, END)
                self.entry_password.insert(0, data["password"])
                self.password_manager.copy_password(data["password"])
            else:
                self.password_manager.notification_manager.show("No existen detalles para ese sitio!", "red")

    def generate_password(self):
        max_length = self.slider_password_length.get()
        max_length = int(float(max_length))
        password = self.password_manager.generate_password(max_length, self.use_letters, self.use_numbers, self.use_symbols)
        self.entry_password.delete(0, END)
        self.entry_password.insert(0, password)

        # Copiar la contraseña al portapapeles
        self.password_manager.copy_password(password)

    def save_password(self):
        website = self.dropdown_sites.get().strip()
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if self.password_manager.save_password(website, username, password):
            self.dropdown_sites.delete(0, END)
            self.entry_password.delete(0, END)
            self.entry_username.delete(0, END)
            self.load_sites()
            self.password_manager.notification_manager.show("Contraseña guardada correctamente!", "green")

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
            self.password_manager.notification_manager.show("No existen detalles para ese sitio!", "red")

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
            self.checkbutton_use_letters.grid(column=1, row=8, sticky="W")
            self.checkbutton_use_numbers.grid(column=1, row=9, sticky="W")
            self.checkbutton_use_symbols.grid(column=1, row=10, sticky="W")
            self.label_password_length.grid(column=0, row=6, sticky="E")
            self.slider_password_length.grid(column=1, row=6, sticky="W")
            self.label_password_strength.grid(column=0, row=5, sticky="E")
            self.label_password_strength_value.grid(column=1, row=5)
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
        strenght = ["Debil", "Medio", "Fuerte", "Muy Fuerte"]
        strenght_colors = ["red", "orange", "green", "#2c69db"]
        
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
            self.password_manager.notification_manager.show(f"No {content_type} para copiar!", "red")
            return
        self.password_manager.notification_manager.show(f"{content_type.capitalize()} copiado al clipboard!", "green")
        copy(content)

    def copy_username(self):
        username = self.entry_username.get()
        self.copy_to_clipboard(username, "username")

    def copy_password(self):
        password = self.entry_password.get()
        self.copy_to_clipboard(password, "password")
