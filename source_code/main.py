import pandas as pd
import csv
from datetime import datetime
from dataEntry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE = "Finance_data.csv"
    CSV_COLUMNS = ["date", "amount", "category", "description"]
    CSV_FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.CSV_COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_csv(cls, date, amount, category, description):
        data_dictionary = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(CSV.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV.CSV_COLUMNS)
            writer.writerow(data_dictionary)
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.CSV_FORMAT)
        start_date = datetime.strptime(start_date, cls.CSV_FORMAT)
        end_date = datetime.strptime(end_date, cls.CSV_FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print(
                f"No transactions occured from {start_date.strftime(cls.CSV_FORMAT)} to {end_date.strftime(cls.CSV_FORMAT)}"
            )
        else:
            print(
                f"Transactions occured from {start_date.strftime(cls.CSV_FORMAT)} to {end_date.strftime(cls.CSV_FORMAT)}"
            )
            print()
            print(
                filtered_df.to_string(
                    index=False,
                    formatters={"date": lambda x: x.strftime(cls.CSV_FORMAT)},
                )
            )

            total_income = filtered_df[filtered_df["category"] == "Income"][
                "amount"
            ].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"][
                "amount"
            ].sum()
            print("\nSummary:")
            print(f"Total Income: Rs.{total_income}")
            print(f"Total Expense: Rs.{total_expense}")
            print(f"Net Savings: Rs.{(total_income-total_expense)}")

        return filtered_df


def get_User_data():
    CSV.initialize_csv()
    date = get_date(
        "Enter date in dd-mm-yyyy format or press Enter for today's date", True
    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_csv(date, amount, category, description)


def plot_Graph(df):
    df.set_index("date", inplace=True)
    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses over time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print()
        print("1. Add Transaction")
        print("2. Get a list of transactions within a date range and a summary")
        print("3. Exit")
        print("Press 1 or 2 or 3")
        choice = int(input("Enter your choice"))

        if choice == 1:
            get_User_data()

        elif choice == 2:
            start_date = get_date("Enter start date in dd-mm-yyyy format")
            end_date = get_date("Enter end date in dd-mm-yyyy format")
            df = CSV.get_transactions(start_date, end_date)

            if input("Do you want to see the plot (y/n)").lower() == "y":
                print()
                plot_Graph(df)

        elif choice == 3:
            print("Exiting...")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
