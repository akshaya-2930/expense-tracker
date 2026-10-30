import csv
from datetime import datetime
import pandas as pd


def add_expense():
    date = input("Date enter chey (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Date format thappu! Ela undali: 2026-10-30")
        return

    category = input("Category enter chey: ").strip()

    try:
        amount = float(input("Amount enter chey: "))

        with open("expenses.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date, category, amount])

        print("Expense save ayyindi! ✅")
    except ValueError:
        print("Amount lo number matrame enter chey!")


def show_total():
    total = 0

    try:
        with open("expenses.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                total = total + float(row[2])
        print("Total kharchu:", total)
    except FileNotFoundError:
        print("Inka expenses emi ledu!")


def show_category_totals():
    totals = {}

    try:
        with open("expenses.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                category = row[1].lower().strip()
                amount = float(row[2])

                if category in totals:
                    totals[category] = totals[category] + amount
                else:
                    totals[category] = amount

        print("Category-wise kharchu:")
        for category, amount in totals.items():
            print(category.capitalize() + ":", amount)
    except FileNotFoundError:
        print("Inka expenses emi ledu!")


def show_monthly_summary():
    try:
        df = pd.read_csv("expenses.csv", header=None, names=["date", "category", "amount"])
        df["category"] = df["category"].str.strip().str.lower()
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        df["month"] = df["date"].dt.strftime("%Y-%m")

        summary = df.groupby("month")["amount"].sum()

        print("Monthly kharchu:")
        for month, amount in summary.items():
            print(month + ":", amount)
    except FileNotFoundError:
        print("Inka expenses emi ledu!")


def main():
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Expense add chey")
        print("2. Total chudu")
        print("3. Category-wise chudu")
        print("4. Monthly summary chudu")
        print("5. Exit")

        choice = input("Nee choice enter chey (1-5): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            show_total()
        elif choice == "3":
            show_category_totals()
        elif choice == "4":
            show_monthly_summary()
        elif choice == "5":
            print("Bye papa! 👋")
            break
        else:
            print("1 nunchi 5 madhya number enter chey!")


main()
