from flask import Flask, request
import mysql.connector

app = Flask(__name__)

# Vulnerable database connection (Hardcoded credentials)
def init_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",      # Hardcoded username
        password="",  # Hardcoded password
        database="test_db"
    )
    return conn

# Vulnerable function - SQL Injection
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = init_db()
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"  # SQL Injection risk
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    if result:
        return f"User Details: {result}"
    return "User not found."

# Vulnerable function - Hardcoded credentials and unsafe string formatting
@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    conn = init_db()
    cursor = conn.cursor()
    query = f"INSERT INTO users (name, email) VALUES ('{name}', '{email}')"  # SQL Injection risk
    cursor.execute(query)
    conn.commit()
    conn.close()
    return "User added successfully."

if __name__ == "__main__":
    app.run(debug=True)
