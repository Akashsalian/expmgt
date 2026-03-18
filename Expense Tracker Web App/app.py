from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="expense_tracker"
)

cursor = db.cursor()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM transactions")
    data = cursor.fetchall()

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
    income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
    expense = cursor.fetchone()[0] or 0

    balance = income - expense

    return render_template("index.html", data=data, income=income, expense=expense, balance=balance)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        t_type = request.form['type']
        amount = request.form['amount']
        category = request.form['category']

        query = "INSERT INTO transactions (type, amount, category) VALUES (%s, %s, %s)"
        cursor.execute(query, (t_type, amount, category))
        db.commit()

        return redirect('/')

    return render_template("add.html")


@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM transactions WHERE id=%s", (id,))
    db.commit()
    return redirect('/')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        t_type = request.form['type']
        amount = request.form['amount']
        category = request.form['category']

        query = "UPDATE transactions SET type=%s, amount=%s, category=%s WHERE id=%s"
        cursor.execute(query, (t_type, amount, category, id))
        db.commit()

        return redirect('/')

    cursor.execute("SELECT * FROM transactions WHERE id=%s", (id,))
    data = cursor.fetchone()

    return render_template("edit.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)