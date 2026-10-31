from flask import Flask, render_template_string, request, redirect
import csv

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Expense Tracker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0f2f5;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 700px;
            margin: auto;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        .total {
            font-size: 24px;
            font-weight: bold;
            color: #2e7d32;
        }
        input {
            padding: 8px;
            margin: 4px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            padding: 8px 16px;
            background: #4caf50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background: #388e3c;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th {
            background: #4caf50;
            color: white;
            padding: 10px;
            text-align: left;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #eee;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Expense Tracker</h1>

        <div class="card">
            <p>Total kharchu</p>
            <p class="total">Rs. {{ total }}</p>
        </div>

        <div class="card">
            <h2>Add Expense</h2>
            <form method="POST">
                <input type="date" name="date" required>
                <input type="text" name="category" placeholder="Category" required>
                <input type="number" step="0.01" name="amount" placeholder="Amount" required>
                <button type="submit">Add</button>
            </form>
        </div>

        <div class="card">
            <h2>Expenses</h2>
            <table>
                <tr>
                    <th>Date</th>
                    <th>Category</th>
                    <th>Amount</th>
                </tr>
                {% for e in expenses %}
                <tr>
                    <td>{{ e[0] }}</td>
                    <td>{{ icons.get(e[1].strip().lower(), "💰") }} {{ e[1] }}</td>
                    <td>{{ e[2] }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </div>
</body>
</html>
"""

icons = {
    "food": "🍔",
    "travel": "✈️",
    "books": "📚",
    "shopping": "🛍️",
    "movies": "🎬",
}


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        date = request.form["date"]
        category = request.form["category"].strip()
        amount = float(request.form["amount"])

        with open("expenses.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date, category, amount])

        return redirect("/")

    total = 0
    expenses = []
    try:
        with open("expenses.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                expenses.append(row)
                total = total + float(row[2])
    except FileNotFoundError:
        pass

    return render_template_string(PAGE, total=total, expenses=expenses, icons=icons)


if __name__ == "__main__":
    app.run(debug=True)