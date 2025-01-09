from datetime import datetime

DATE_FORMAT = "%d-%m-%Y"
TRANSACTION_TYPES = {"I": "Income", "E": "Expense"}


def enter_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(DATE_FORMAT)
    try:
        valid_date = datetime.strptime(date_str, DATE_FORMAT)
        return valid_date.strftime(DATE_FORMAT)
    except ValueError:
        print("Invalid format. Use dd-mm-yyyy.")
        return enter_date(prompt, allow_default)


def enter_amount():
    try:
        amount = float(input("Enter transaction amount: "))
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        return amount
    except ValueError as e:
        print(e)
        return enter_amount()


def enter_category():
    transaction_type = input("Enter 'I' for Income or 'E' for Expense: ").upper()
    if transaction_type in TRANSACTION_TYPES:
        return TRANSACTION_TYPES[transaction_type]
    print("Invalid input. Please enter 'I' or 'E'.")
    return enter_category()


def enter_note():
    return input("Enter additional details (optional): ")
