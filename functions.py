from datetime import datetime
from dialog_functions import ask, info, category_select
class Transaction:
    def __init__(self, amount, date, description):
        self.amount = amount
        self.date = date
        self.description = description

def get_user_input(file_name):

    categories = ['income', 'expense']

    category_dialog = category_select(categories)
    category_dialog.wait_window()

    category = category_dialog.selected_category

    if category is None:
        return None

    amount_str = ask("Amount", "Enter the amount:")
    try:
        amount = float(amount_str)
    except ValueError:
        info("Amount Error.", "Please enter a valid amount.")
        return None

    try:
        date = datetime.strptime(ask("Date", "Enter the date (YYYY.MM.DD):"), "%Y.%m.%d").date()
    except ValueError:
        info("Date Error", "Please enter a valid date (YYYY.MM.DD).")
        return None

    description = ask("Description", "Enter a description:")

    try:
        with open(file_name, 'a') as file:
            if category == 'income':
                file.write(f'{amount},{date},{description}\n')
            elif category == 'expense':
                file.write(f'{-amount},{date},{description}\n')
    except IOError:
        info("Error adding transaction. Cannot access a file.")

    return 

def read_file(file_name):
    transactions = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                data = [item.strip() for item in line.strip().split(',')]
                if len(data) == 3:  
                    date_str = data[1]
                    try:
                        date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    except ValueError:
                        continue
                    transaction = Transaction(float(data[0]), date, data[2])
                    transactions.append(transaction)
    except IOError:
        file = open('transactions.txt', 'x')
    return transactions

def enter_target_date():
    try:
        year = ask("Year", "Enter the year:")
        year = int(year)
    except ValueError:
        info("Invalid Year", "Invalid year. Please enter a valid number.")
        return

    month_name = ask("Month", "Enter the name of the month:")
    try:
        target_date = datetime(year, datetime.strptime(month_name, "%B").month, 1).date()
    except ValueError:
        print("Invalid month name. Please enter a valid month.")

    return target_date, month_name, year

def balance():
    transactions = read_file('transactions.txt')
    current_balance = sum(transaction.amount for transaction in transactions)
    return f"\nYour current balance is: {current_balance:.2f}"

def monthly_balance():
    transactions = read_file('transactions.txt')
    if read_file('transactions.txt') == []:
        info("No transactions.", "Add transactions to see the monthly balance.")
        return None
    else:
        target_date, month_name, year = enter_target_date()

    month_balance = sum(
        transaction.amount 
        for transaction in transactions
        if transaction.date is not None and transaction.date >= target_date
    )

    return f"\nYour balance in {month_name} {year} was: {month_balance:.2f}"

def month_summary():
    transactions = read_file('transactions.txt')

    if read_file('transactions.txt') == []:
        info("No transactions.", "Add transactions to see the monthly balance.")
        return None
    else:
        target_date, month_name, year = enter_target_date()
    
    start_of_month = target_date.replace(day=1)
    end_of_month = start_of_month.replace(
        month=start_of_month.month + 1 if start_of_month.month < 12 else 1,
        year=start_of_month.year + 1 if start_of_month.month == 12 else start_of_month.year,
        day=1
    )

    summary_balance = sum(
        transaction.amount
        for transaction in transactions
        if (
            transaction.date is not None
            and start_of_month <= transaction.date < end_of_month
        )
    )

    income_transactions = [transaction for transaction in transactions if transaction.amount > 0]
    expense_transactions = [transaction for transaction in transactions if transaction.amount < 0]

    income_list = []
    expense_list = []

    for transaction in income_transactions:
        if (
            transaction.date is not None
            and start_of_month <= transaction.date < end_of_month
        ):
            line = (
                f'Amount: +{transaction.amount:.2f}, '
                f'Date: {transaction.date}, '
                f'Description: {transaction.description}'
            )
            income_list.append(line.ljust(80))

    for transaction in expense_transactions:
        if (
            transaction.date is not None
            and start_of_month <= transaction.date < end_of_month
        ):
            line = (
                f'Amount: {transaction.amount:.2f}, '
                f'Date: {transaction.date}, '
                f'Description: {transaction.description}'
            )
            expense_list.append(line.ljust(80))

    result = (
        f'\nIncome transactions for {start_of_month.strftime("%Y.%m")}:\n\n' +
        '\n'.join(income_list) +
        f'\n\nExpense transactions for {start_of_month.strftime("%Y.%m")}:\n\n' +
        '\n'.join(expense_list) +
        f'\n\nThe change in your monthly balance for {month_name} {year} was: {summary_balance:.2f}'
    )
    return result

def transactions_range():
    transactions = read_file('transactions.txt')
    if read_file('transactions.txt') == []:
        info("No transactions.", "Add transactions to see the monthly balance.")
        return None
    else:
        start_date_str = ask("Start Date", "Enter the start date (YYYY.MM.DD):")
        end_date_str = ask("End Date", "Enter the end date (YYYY.MM.DD):")

    try:
        start_date = datetime.strptime(start_date_str, "%Y.%m.%d").date()
        end_date = datetime.strptime(end_date_str, "%Y.%m.%d").date()
    except ValueError:
        info("Date Error", "Please enter valid start and end dates (YYYY.MM.DD).")
        return

    transactions_range = [
        transaction
        for transaction in transactions
        if transaction.date is not None and start_date <= transaction.date <= end_date
    ]

    if not transactions_range:
        info("No Transactions", f"There are no transactions between {start_date} and {end_date}.")
        return

    transaction_history = []
    for transaction in transactions_range:
        line = (
            f'Amount: {transaction.amount:.2f}, '
            f'Date: {transaction.date}, '
            f'Description: {transaction.description}'
        )
        transaction_history.append(line.ljust(80))

    result = (
        f'\nTransactions between {start_date} and {end_date}:\n\n' +
        '\n'.join(transaction_history)
    )

    return result



