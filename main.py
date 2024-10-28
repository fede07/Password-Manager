import json
from tkinter import Tk, Button, Label, Canvas, PhotoImage, Entry, END, messagebox, Scale
from random import choice, shuffle, randint
from pyperclip import copy
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    strenght = ["Weak", "Medium", "Strong", "Very Strong"]
    
    max_length = slider_password_lenght.get()

    num_letters = max(4, max_length // 2)  # Al menos 4 letras o la mitad de la longitud
    num_symbols = max(1, max_length // 6)  # Al menos 1 símbolo
    num_numbers = max_length - num_letters - num_symbols

    password_letters = [choice(letters) for _ in range(num_letters)]
    password_symbols = [choice(symbols) for _ in range(num_symbols)]
    password_numbers = [choice(numbers) for _ in range(num_numbers)]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)

    password =  ''.join(password_list)
    
    if len(password) < 8:
        label_password_strength_value.config(text=strenght[0])
    elif len(password) < 10:
        label_password_strength_value.config(text=strenght[1])
    elif len(password) < 12:
        label_password_strength_value.config(text=strenght[2])
    else:
        label_password_strength_value.config(text=strenght[3])

    entry_password.delete(first=0, last=END)
    entry_password.insert(0, password)

    copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():

    website = entry_website.get().strip()
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showwarning(title="Empty entry!", message="One or more entries are empty!")
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
#-----------------------------SEARCH PASSWORD---------------------------#

def search_password():

    website = entry_website.get()
    data = None

    try:
        with open(file="data.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showwarning(title="Save file not found", message="No passwords have been saved yet!")      
    else:
        if website in data:
            email=data[website]["email"]
            password=data[website]["password"]
            messagebox.showinfo(title=website, message=f"Username: {email}\nPassword:{password}")
        else:
            messagebox.showinfo(title=website, message="Website not saved!")
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

label_password_strength_value = Label(text="Weak")
label_password_strength_value.grid(column=1, row=4, sticky="W")

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
button_add.grid(column=0, row=6, columnspan=3, sticky="W")

#Sliders

slider_password_lenght = Scale(from_=1, to=32, orient="horizontal", length=200)
slider_password_lenght.grid(column=1, row=5, sticky="W")

window.mainloop()