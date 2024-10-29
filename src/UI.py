from tkinter import Button, Label, Canvas, PhotoImage, Entry, END, Scale, Checkbutton, IntVar
from pyperclip import copy


class UI:
    
    def __init__(self, window, password_manager):
        self.window = window
        self.password_manager = password_manager
        self.logo_img = PhotoImage(file="assets/logo.png")
        self.create_widgets()

    def create_widgets(self):
        self.window.title("Password Manager")
        self.window.config(padx=20, pady=20)
        self.window.minsize(width=480, height=420)

        canvas = Canvas(width=200, height=200, highlightthickness=0)
        canvas.create_image(100, 100, image=self.logo_img)
        canvas.grid(column=1, row=0)

        # Labels
        self.label_website = Label(text="Website:")
        self.label_website.grid(column=0, row=1, sticky="E")

        self.label_username = Label(text="Email/Username:")
        self.label_username.grid(column=0, row=2, sticky="E")

        self.label_password = Label(text="Password:")
        self.label_password.grid(column=0, row=3, sticky="E")

        self.label_password_strength = Label(text="Password Strength:")

        self.label_password_strength_value = Label(text="")

        self.label_password_length = Label(text="Password Length:")
        self.label_notification = Label(text="", width=60)
        self.label_notification.forget()

        # Entries
        self.entry_website = Entry(width=30)
        self.entry_website.grid(column=1, row=1, sticky="W", columnspan=1)
        self.entry_website.focus()

        self.entry_username = Entry(width=30)
        self.entry_username.grid(column=1, row=2, sticky="W", columnspan=1)

        self.entry_password = Entry(width=30)
        self.entry_password.grid(column=1, row=3, sticky="W", columnspan=1)

        # Buttons
        button_search = Button(text="Search", command=self.search_password, width=15)
        button_search.grid(column=2, row=1, sticky="W")

        button_generate_pass = Button(text="Generate Password", command=self.generate_password, width=15)
        button_generate_pass.grid(column=2, row=3, sticky="W")

        button_add = Button(text="Add", width=60, command=self.save_password)
        button_add.grid(column=0, row=10, columnspan=3, sticky="W")

        self.toggle_button = Button(text="More Options", width=15, command=self.toggle_options)
        self.toggle_button.grid(column=2, row=4, sticky="W")
        
        self.button_copy_username = Button(text="Copy Username", width=15, command=self.copy_username)
        self.button_copy_username.grid(column=1, row=11, sticky="E")
        
        self.button_copy_password = Button(text="Copy Password", width=15, command=self.copy_password)
        self.button_copy_password.grid(column=2, row=11)

        # Sliders
        self.slider_password_length = Scale(from_=4, to=32, orient="horizontal", length=200, showvalue=8, command=self.on_slider_change)
        self.slider_password_length.set(12)

        # CheckButtons
        self.use_letters = IntVar(value=1)
        self.use_numbers = IntVar(value=1)
        self.use_symbols = IntVar(value=1)

        self.checkbutton_use_letters = Checkbutton(text="Use letters", variable=self.use_letters, command=self.validate_checkbuttons)
        self.checkbutton_use_numbers = Checkbutton(text="Use numbers", variable=self.use_numbers, command=self.validate_checkbuttons)
        self.checkbutton_use_symbols = Checkbutton(text="Use symbols", variable=self.use_symbols, command=self.validate_checkbuttons)

        # Visibility
        self.options_visible = False

    def generate_password(self):
        max_length = self.slider_password_length.get()
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
        strenght_colors = ["red", "orange", "green", "blue"]
        if int(value) <= 6:
            self.label_password_strength_value.config(text=strenght[0], fg=strenght_colors[0], font=("Arial", 10, "bold"))
        elif int(value) <= 10:
            self.label_password_strength_value.config(text=strenght[1], fg=strenght_colors[1], font=("Arial", 10, "bold"))
        elif int(value) < 12:
            self.label_password_strength_value.config(text=strenght[2], fg=strenght_colors[2], font=("Arial", 10, "bold"))
        else:
            self.label_password_strength_value.config(text=strenght[3], fg=strenght_colors[3], font=("Arial", 10, "bold"))
            
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
