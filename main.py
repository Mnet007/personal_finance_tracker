import pandas as pd
import csv
from datetime import datetime
from data_entry import enter_amount, enter_category, enter_date, enter_note
import matplotlib.pyplot as plt


class TransactionManager:
    DATA_FILE = "finance_data.csv"
    HEADERS = ["transaction_date", "transaction_amount", "transaction_type", "details"]
    DATE_FORMAT = "%d-%m-%Y"

    @classmethod
    def setup_csv(cls):
        try:
            pd.read_csv(cls.DATA_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.HEADERS)
            df.to_csv(cls.DATA_FILE, index=False)

    @classmethod
    def record_transaction(cls, transaction_date, transaction_amount, transaction_type, details):
        new_record = {
            "transaction_date": transaction_date,
            "transaction_amount": transaction_amount,
            "transaction_type": transaction_type,
            "details": details,
        }
        with open(cls.DATA_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.HEADERS)
            writer.writerow(new_record)
        print("Transaction recorded successfully")

    @classmethod
    def filter_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.DATA_FILE)
        df["transaction_date"] = pd.to_datetime(df["transaction_date"], format=cls.DATE_FORMAT)
        start_date = datetime.strptime(start_date, cls.DATE_FORMAT)
        end_date = datetime.strptime(end_date, cls.DATE_FORMAT)

        filtered_df = df[(df["transaction_date"] >= start_date) & (df["transaction_date"] <= end_date)]

        if filtered_df.empty:
            print("No transactions found in this date range.")
        else:
            print(f"Transactions between {start_date.strftime(cls.DATE_FORMAT)} and {end_date.strftime(cls.DATE_FORMAT)}")
            print(filtered_df.to_string(index=False))
            
            total_income = filtered_df[filtered_df["transaction_type"] == "Income"]["transaction_amount"].sum()
            total_expense = filtered_df[filtered_df["transaction_type"] == "Expense"]["transaction_amount"].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Balance: ${(total_income - total_expense):.2f}")

        return filtered_df


def add_transaction():
    TransactionManager.setup_csv()
    transaction_date = enter_date("Enter transaction date (dd-mm-yyyy) or press Enter for today: ", allow_default=True)
    transaction_amount = enter_amount()
    transaction_type = enter_category()
    details = enter_note()
    TransactionManager.record_transaction(transaction_date, transaction_amount, transaction_type, details)


def plot_data(df):
    df.set_index("transaction_date", inplace=True)

    income_df = (
        df[df["transaction_type"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["transaction_type"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 6))
    plt.plot(income_df.index, income_df["transaction_amount"], label="Income", color="blue")
    plt.plot(expense_df.index, expense_df["transaction_amount"], label="Expense", color="orange")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income vs Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n1. Record a new transaction")
        print("2. View transactions summary")
        print("3. Exit")
        choice = input("Select an option (1-3): ")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            start_date = enter_date("Enter start date (dd-mm-yyyy): ")
            end_date = enter_date("Enter end date (dd-mm-yyyy): ")
            df = TransactionManager.filter_transactions(start_date, end_date)
            if not df.empty and input("Would you like to visualize the data? (y/n): ").lower() == "y":
                plot_data(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid input. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
