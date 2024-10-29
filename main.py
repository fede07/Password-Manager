import json
from tkinter import Tk, Button, Label, Canvas, PhotoImage, Entry, END, messagebox, Scale, Checkbutton, IntVar
from random import choice, shuffle, randint
from pyperclip import copy

# --------------------------- NOTIFICATION MESSAGE ------------------------------ #

def show_notification(message, color):
    label_notification.config(text=message, fg=color)
    label_notification.grid(column=0, row=11, sticky="W", columnspan=3)

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    
    max_length = slider_password_lenght.get()
    password_list = []

    # Asegurarse de incluir al menos un carácter de cada tipo seleccionado
    if use_letters.get() == 1:
        password_list.append(choice(letters))
    if use_numbers.get() == 1:
        password_list.append(choice(numbers))
    if use_symbols.get() == 1:
        password_list.append(choice(symbols))

    # Completar el resto de la contraseña con caracteres aleatorios según las opciones seleccionadas
    while len(password_list) < max_length:
        if use_letters.get() == 1:
            password_list.append(choice(letters))
        if use_numbers.get() == 1:
            password_list.append(choice(numbers))
        if use_symbols.get() == 1:
            password_list.append(choice(symbols))
            
    # Calcular la fortaleza de la contraseña
    on_slider_change(max_length)

    # Limitar el tamaño total a max_length y mezclar los caracteres
    password_list = password_list[:max_length]
    shuffle(password_list)
    password = ''.join(password_list)

    # Mostrar la contraseña en el campo de entrada
    entry_password.delete(first=0, last=END)
    entry_password.insert(0, password)

    # Copiar la contraseña al portapapeles
    copy_password()

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():

    website = entry_website.get().strip()
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        label_notification.config(text="Please fill all the fields!", fg="red")
        return

    is_ok = messagebox.askokcancel(title=website, message=f"Are these details correct?\nUsername: {username}\nPassword: {password}\n")

    if is_ok:

        data = None

        new_data = {
            website: {
                "email": username,
                "password": password
            }
        }

        try:
            with open(file="data.json", mode="r") as saved_data:
                data = json.load(saved_data)
                data.update(new_data)
        except FileNotFoundError:
            with open(file="data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open(file="data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)


        entry_website.delete(first=0, last=END)
        entry_password.delete(first=0, last=END)
        entry_username.delete(first=0, last=END)
        
        show_notification("Password saved successfully!", "green")
        
        
#-----------------------------COPY PASSWORD-----------------------------#

def copy_password():
    password = entry_password.get()
    copy(password)
    show_notification("Password copied to clipboard!", "green")
    
        
#-----------------------------SEARCH PASSWORD---------------------------#

def search_password():

    website = entry_website.get()
    data = None

    try:
        with open(file="data.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        show_notification("No Data File Found!", "red")      
    else:
        if website in data:
            email=data[website]["email"]
            password=data[website]["password"]
            entry_username.delete(first=0, last=END)
            entry_username.insert(0, email)
            entry_password.delete(first=0, last=END)
            entry_password.insert(0, password)
            copy_password()
        else:
            show_notification("No details for the website exist!", "red")
            
#-----------------------------VALIDATE CHECKBUTTONS---------------------------#
            
def validate_checkbuttons():
    # Contar los checkbuttons seleccionados
    selected_options = sum([use_letters.get(), use_numbers.get(), use_symbols.get()])
    
    # Si solo queda uno seleccionado, bloquearlo
    if selected_options == 1:
        if use_letters.get() == 1:
            checkbutton_use_letters.config(state="disabled")
        elif use_numbers.get() == 1:
            checkbutton_use_numbers.config(state="disabled")
        elif use_symbols.get() == 1:
            checkbutton_use_symbols.config(state="disabled")
    else:
        # Si hay más de uno, asegurarse de que todos estén habilitados
        checkbutton_use_letters.config(state="normal")
        checkbutton_use_numbers.config(state="normal")
        checkbutton_use_symbols.config(state="normal")
        
options_visible = False
        
def toggle_options():
    global options_visible
    if options_visible:
        # Ocultar los checkbox
        checkbutton_use_letters.grid_forget()
        checkbutton_use_numbers.grid_forget()
        checkbutton_use_symbols.grid_forget()
        slider_password_lenght.grid_forget()
        label_password_lenght.grid_forget()
    else:
        # Mostrar los checkbox
        checkbutton_use_letters.grid(column=1, row=7, sticky="W")
        checkbutton_use_numbers.grid(column=1, row=8, sticky="W")
        checkbutton_use_symbols.grid(column=1, row=9, sticky="W")
        slider_password_lenght.grid(column=1, row=5, sticky="W")
        label_password_lenght.grid(column=0, row=5, sticky="E")

    options_visible = not options_visible  
    
    if options_visible:
        toggle_button.config(text="Less Options")
    else:
        toggle_button.config(text="More Options")
        
# ------------------------- SLIDER METHODS ---------------------------- #

def on_slider_change(value):
    strenght = ["Weak", "Medium", "Strong", "Very Strong"]
    strenght_colors = ["red", "orange", "green", "blue"]
    if int(value) <= 6:
        label_password_strength_value.config(text=strenght[0], fg=strenght_colors[0], font=("Arial", 10, "bold"))
    elif int(value) <= 10:
        label_password_strength_value.config(text=strenght[1], fg=strenght_colors[1], font=("Arial", 10, "bold"))
    elif int(value) < 12:
        label_password_strength_value.config(text=strenght[2], fg=strenght_colors[2], font=("Arial", 10, "bold"))
    else:
        label_password_strength_value.config(text=strenght[3], fg=strenght_colors[3], font=("Arial", 10, "bold"))
        
        
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)
window.minsize(width=460, height=400)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

#Labels
label_website = Label(text="Website:")
label_website.grid(column=0, row=1, sticky="E")


label_username = Label(text="Email/Username:")
label_username.grid(column=0, row=2, sticky="E")

label_password = Label(text="Password:")
label_password.grid(column=0, row=3, sticky="E")

label_password_strength = Label(text="Password Strength:")
label_password_strength.grid(column=0, row=4, sticky="E")

label_password_strength_value = Label(text="")
label_password_strength_value.grid(column=1, row=4, sticky="W")

label_password_lenght = Label(text="Password Lenght:")

label_notification = Label(text="", width=60)
label_notification.forget()

#Entries
entry_website = Entry(width=30)
entry_website.grid(column=1, row=1,sticky="W", columnspan=1)
entry_website.focus()

entry_username = Entry(width=30)
entry_username.grid(column=1, row=2, sticky="W", columnspan=1)
entry_username.insert(0, "")

entry_password = Entry(width=30)
entry_password.grid(column=1, row=3, sticky="W", columnspan=1)

#Buttons

button_search = Button(text="Search", command=search_password, width=15)
button_search.grid(column=2, row=1, sticky="W")

button_generate_pass = Button(text="Generate Password", command=generate_password, width=15)
button_generate_pass.grid(column=2, row=3, sticky="W")

button_add = Button(text="Add", width=60, command=save)
button_add.grid(column=0, row=10, columnspan=3, sticky="W")

toggle_button = Button(text="More Options", width=15, command=toggle_options)
toggle_button.grid(column=2, row=4, sticky="W")

#Sliders

slider_password_lenght = Scale(from_=4, to=32, orient="horizontal", length=200, showvalue=8, command=on_slider_change)
slider_password_lenght.set(12)

#CheckButtons

use_letters = IntVar(value=1)
use_numbers = IntVar(value=1)
use_symbols = IntVar(value=1)

checkbutton_use_letters = Checkbutton(text="Use letters", variable=use_letters, command=validate_checkbuttons)

checkbutton_use_numbers = Checkbutton(text="Use numbers", variable=use_numbers, command=validate_checkbuttons)  

checkbutton_use_symbols = Checkbutton(text="Use symbols", variable=use_symbols, command=validate_checkbuttons)

if use_symbols.get() == 0 and use_numbers.get() == 0 and use_letters.get() == 0:
    checkbutton_use_letters.setvar(1)

#-----------------------------MAINLOOP---------------------------#

window.mainloop()

