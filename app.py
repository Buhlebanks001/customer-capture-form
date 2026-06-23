from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database and table
def init_db():
    conn = sqlite3.connect("customers.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# Home Page
@app.route("/")
def home():

    conn = sqlite3.connect("customers.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        customers=customers
    )

# Add Customer
@app.route("/add", methods=["POST"])
def add_customer():

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    phone = request.form["phone"]

    conn = sqlite3.connect("customers.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO customers
        (first_name, last_name, email, phone)
        VALUES (?, ?, ?, ?)
    """, (first_name, last_name, email, phone))

    conn.commit()
    conn.close()

    return redirect("/")

# Delete Customer
@app.route("/delete/<int:id>")
def delete_customer(id):

    conn = sqlite3.connect("customers.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM customers WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)