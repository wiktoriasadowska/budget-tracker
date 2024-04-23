import tkinter as tk
from tkinter import Label, Button, font
from functions import get_user_input, balance, monthly_balance, month_summary, transactions_range

def handle_add():
    clear_result_label()
    get_user_input('transactions.txt')
    balance_label.config(text=balance())

def handle_monthly_balance():
    clear_result_label()
    result_label.config(text=monthly_balance(), font=font_size)

def handle_month_summary():
    clear_result_label()
    result_label.config(text=month_summary(), font=font_size)

def handle_transactions_range():
    clear_result_label()
    result_label.config(text=transactions_range(), font=font_size)
  
def clear_result_label():
    result_label.config(text="")

def set_dark_mode():
    root.config(bg="#000")
    menu_label.config(bg="#000", fg="#fff")
    result_label.config(bg="#000", fg="#fff")

    for button in [add_button, monthly_balance_button, summary_button, history_button]:
        button.config(bg="#000", fg="#333", width=30, height=2, font=font_size)

root = tk.Tk()
root.title("Budget Tracker")

window_width = 1000
window_height = 1000

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

button_padding = 10
font_size=font.Font(size=16)

title_label = Label(root, text="Hello!", font=('Helvetica', 50, 'bold'), bg="black", fg="white")
title_label.pack()

balance_label = Label(root, text=balance(), font=('Helvetica', 30, 'bold'), bg="black", fg="pink")
balance_label.pack()

result_label = Label(root, text="", font=font.Font(size=12), bg="black")
result_label.pack()

menu_label = Label(root, text="What do you want to do?", font=font_size)
menu_label.pack()

add_button = Button(root, text="Add Transaction", command=handle_add)
add_button.pack(pady=button_padding)

monthly_balance_button = Button(root, text="See Monthly Balance", command=handle_monthly_balance)
monthly_balance_button.pack(pady=button_padding)

summary_button = Button(root, text="See Month Summary", command=handle_month_summary)
summary_button.pack(pady=button_padding)

history_button = Button(root, text="See Transactions History", command=handle_transactions_range)
history_button.pack(pady=button_padding)

exit_button = Button(root, text="Exit", command=root.destroy, width=8, height=2, bg="#000", fg="#333")
exit_button.pack(pady=15)

result_label = Label(root, text="", font=font.Font(size=12), bg="black")
result_label.pack()

set_dark_mode()

root.mainloop()


