
class NotificationManager:
    
    def __init__(self, label, style):
        self.label = label
        self.style = style

    def show(self, message, color):
        self.label.config(text=message, foreground=color, background=self.style.bg_color)
        self.label.grid(column=0, row=13, columnspan=4, sticky="news", pady=(5, 5))
