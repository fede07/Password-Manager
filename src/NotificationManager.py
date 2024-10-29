class NotificationManager:
    
    def __init__(self, label):
        self.label = label

    def show(self, message, color):
        self.label.config(text=message, fg=color)
        self.label.grid(column=0, row=13, columnspan=3)
