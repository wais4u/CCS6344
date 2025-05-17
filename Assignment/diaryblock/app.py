from flask import Flask, request, render_template, redirect, url_for
import pyodbc

app = Flask(__name__)

# Configure your DB connection here
conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=diary_app;"        # Replace with your actual DB name
    "Trusted_Connection=yes;"
    "Encrypt=no"
)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

            # Match both username and password directly (NOT recommended for production)
            cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()

            if user:
                return "Login successful!"
            else:
                return "Invalid username or password."

        except Exception as e:
            return f"Login failed: {e}"

        finally:
            conn.close()

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            conn.commit()
            conn.close()
            return "Registration successful!"
        except Exception as e:
            return f"Registration failed: {e}"

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)