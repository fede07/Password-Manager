from tkinter import ttk


class UICreator:
    
    @staticmethod
    def create_button(root, text, command, width, row, column, sticky, columnspan):
        button = ttk.Button(root, text=text, style="Modern.TButton", command=command, width=width)
        button.grid(row=row, column=column, pady=10, sticky=sticky, columnspan=columnspan)
        return button
    
    @staticmethod
    def create_label(root, text, row, column, sticky, width, columnspan):
        label = ttk.Label(root, text=text, style="Modern.TLabel", width=width)
        label.grid(row=row, column=column, sticky=sticky, columnspan=columnspan)
        return label
    
    @staticmethod
    def create_entry(root, width, row, column, sticky, columnspan):
        entry = ttk.Entry(root, width=width, style="Modern.TEntry")
        entry.grid(row=row, column=column, sticky=sticky, columnspan=columnspan)
        return entry
    
    @staticmethod
    def create_checkbutton(root, text, variable, command):
        checkbutton = ttk.Checkbutton(root, text=text, variable=variable, command=command, style="Modern.TCheckbutton")
        return checkbutton

    
    @staticmethod
    def create_combobox(root, values, width, row, column, sticky, columnspan):
        combobox = ttk.Combobox(root, values=values, width=width, style="Modern.TCombobox")
        combobox.grid(row=row, column=column, sticky=sticky, columnspan=columnspan)
        return combobox

