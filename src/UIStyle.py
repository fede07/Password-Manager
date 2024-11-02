from tkinter import ttk

class UIStyle:
    
    def __init__(self, root):
        # Colores y fuentes para el diseño alternativo
        self.bg_color = "#F7F8FA"               # Fondo claro
        self.button_color = "#D3D3D3"           # Azul pastel para botones
        self.button_hover_color = "#3A7CA5"     # Azul ligeramente más oscuro en hover
        self.text_color = "#333333"             # Texto oscuro para contraste
        self.entry_bg_color = "#E4E6E9"         # Fondo de entradas
        self.scale_trough_color = "#82C4B6"     # Verde menta en el trough del slider
        self.font = ("Arial", 11)

        # Configurar el fondo de la ventana
        root.configure(bg=self.bg_color)

        # Configuración de estilos usando ttk.Style
        style = ttk.Style()
        style.theme_use("clam")

        # Estilo del botón
        style.configure(
            "Modern.TButton",
            font=self.font,
            background=self.button_color,
            foreground=self.text_color,
            borderwidth=1,
            #padding=8,
            relief="flat"                       # Bordes planos
        )
        style.map(
            "Modern.TButton",
            background=[("active", self.button_hover_color)],
            relief=[("active", "groove")]
        )

        # Estilo de las etiquetas (labels)
        style.configure(
            "Modern.TLabel",
            font=("Arial", 10),
            background=self.bg_color,
            foreground=self.text_color,
            padding=5
        )

        # Estilo de las entradas de texto (entries)
        style.configure(
            "Modern.TEntry",
            font=self.font,
            fieldbackground=self.entry_bg_color,
            foreground=self.text_color,
            bordercolor=self.scale_trough_color,
            padding=6
        )

        # Estilo del slider (scale)
        style.configure(
            "Modern.TScale",
            background=self.bg_color,
            troughcolor=self.scale_trough_color,
            sliderrelief="flat",
            sliderlength=15
        )

        # Estilo del checkbox
        style.configure(
            "Modern.TCheckbutton",
            font=("Arial", 10),
            background=self.bg_color,
            foreground=self.text_color,
            padding=5,
            borderwidth=0
        )
        
        style.configure(
            "Modern.TCombobox",
            fieldbackground="white",
            background="lightblue",
            foreground="black",
            borderwidth=1,
            relief="solid",
            selectbackground="lightgray",
            selectforeground="blue",
            padding=(5, 5)  # Ajusta el padding vertical para aumentar la altura
        )
