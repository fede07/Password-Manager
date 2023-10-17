import json
from tkinter import Tk, Button, Label, Canvas, PhotoImage, Entry, END, messagebox
from random import choice, shuffle, randint
from pyperclip import copy
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8,10))]
    password_symbols = [choice(symbols) for _ in range(randint(2,4))]
    password_numbers = [choice(numbers) for _ in range(randint(2,4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)

    password =  ''.join(password_list)

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

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

#Labels
label_website = Label(text="Website:")
label_website.grid(column=0, row=1)

label_username = Label(text="Email/Username:")
label_username.grid(column=0, row=2)

label_password = Label(text="Password:")
label_password.grid(column=0, row=3)

#Entries
entry_website = Entry(width=25)
entry_website.grid(column=1, row=1)
entry_website.focus()

entry_username = Entry(width=44)
entry_username.grid(column=1, row=2, columnspan=2)
entry_username.insert(0, "email@gmail.com")

entry_password = Entry(width=26)
entry_password.grid(column=1, row=3)

#Buttons

button_search = Button(text="Search", command=search_password)
button_search.grid(column=2, row=1)

button_generate_pass = Button(text="Generate Password", command=generate_password)
button_generate_pass.grid(column=2, row=3)

button_add = Button(text="Add", width=37, command=save)
button_add.grid(column=1, row=4, columnspan=2)

window.mainloop()