class NotificationManager:
    
    def __init__(self, label, style):
        self.label = label
        self.style = style

    def show(self, message, color):
        self.label.config(text=message, fg=color, bg=self.style.button_color)
        self.label.grid(column=0, row=13, columnspan=3)
