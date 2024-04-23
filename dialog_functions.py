import tkinter as tk
from tkinter import simpledialog, messagebox

class category_select(tk.Toplevel):
    def __init__(self, categories):
        super().__init__()

        self.title("Select Category")

        self.selected_category = None

        for category in categories:
            button = tk.Button(self, text=category, command=lambda c=category: self.set_category(c))
            button.pack()

        self.update_idletasks()
        width = 200
        height = 100
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def set_category(self, category):
        self.selected_category = category
        self.destroy()

def ask(label, text):
    return simpledialog.askstring(label, text)


def info(label, text):
    return messagebox.showinfo(label, text)