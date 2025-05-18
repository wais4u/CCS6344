from flask import Flask, request, render_template, redirect, url_for, session
from datetime import datetime

import pyodbc
import bcrypt

app = Flask(__name__)

app.secret_key = 'ryoiki-tenkai-internship'  # Required for using sessions

# Configure your DB connection here
conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=diary_app;"        # Replace with your actual DB name
    "UID=diaryblockuser;"
    "PWD=D1aryBl0ck01;"
    #"Trusted_Connection=yes;"
    "Encrypt=no"
)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        raw_password = request.form['password']


        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

            cursor.execute("SELECT User_ID, Password FROM Users WHERE username = ?", (username,))
            user = cursor.fetchone()

            #return user[1]

            if user and bcrypt.checkpw(raw_password.encode('utf-8'), user[1].encode('utf-8')):
                session['username'] = username
                #return "Login successful!"
                return redirect(url_for('home_page'))
            else:
                return '''
                        <h2>Invalid username or password.</h2>
                        <p><a href="/login">Click here to return to login page</a></p>
                    '''

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
        raw_password = request.form['password']
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

            # CHECKING IF THE USERNAME OR EMAIL IS TAKEN ALREADY 
            cursor.execute("SELECT * FROM Users WHERE Username = ? OR Email = ?", (username, email))
            existing_user = cursor.fetchone()
            if existing_user:
                return '''
                    <h2>Username or email already taken.</h2>
                    <p><a href="/register">Click here to go back to registration page</a></p>
                '''

            cursor.execute("INSERT INTO Users (Username, Email, Password) VALUES (?, ?, ?)", (username, email, hashed_password))
            conn.commit()
            conn.close()

            return '''
                <h2>Registration successful!</h2>
                <p><a href="/login">Click here to login</a></p>
            '''
        except Exception as e:
            return f"Registration failed: {e}"

    return render_template('register.html')

@app.route('/home')
def home_page():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Get user_id
        cursor.execute("SELECT User_ID FROM Users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            User_ID = user[0]
            cursor.execute("SELECT Entry_ID, Content, Created_at FROM Entries WHERE User_ID = ? ORDER BY Created_At DESC", (User_ID,))
            entries = cursor.fetchall()
            entries = [
                {
                    'entry_id' : e[0],
                    'content': e[1], 
                    'created_at': e[2]
                } 
                for e in entries
            ]
            '''
            entries_dicts = [
                {
                    'entry_id': row.Entry_ID,
                    'content': row.Content,
                    'created_at': row.Created_At
                }
                for row in entries
            ]
            '''
        else:
            entries = []

    except Exception as e:
        return f"Error fetching entries: {e}"

    finally:
        conn.close()

    return render_template('home.html', username=username, entries=entries)

@app.route('/add_entry', methods=['POST'])
def add_entry():
    if 'username' not in session:
        return redirect(url_for('login'))

    content = request.form['content']
    username = session['username']

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Get user_id
        cursor.execute("SELECT User_ID FROM Users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            User_ID = user[0]
            cursor.execute("INSERT INTO Entries (User_ID, Content, Created_At) VALUES (?, ?, ?)", (User_ID, content, datetime.now()))
            conn.commit()

    except Exception as e:
        return f"Error saving entry: {e}"

    finally:
        conn.close()

    return redirect(url_for('home_page'))

@app.route('/delete_entry/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Get user ID
        cursor.execute("SELECT User_ID FROM Users WHERE Username = ?", session['username'])
        user = cursor.fetchone()

        if user:
            cursor.execute("DELETE FROM Entries WHERE Entry_ID = ? AND User_ID = ?", (entry_id, user.User_ID))
            conn.commit()

    except Exception as e:
        return f"Error deleting entry: {e}"

    finally:
        conn.close()

    return redirect(url_for('home_page'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Delete user — will cascade delete entries due to FK with ON DELETE CASCADE
        cursor.execute("DELETE FROM Users WHERE Username = ?", session['username'])
        conn.commit()

        # Clear session after deletion
        session.pop('username', None)

    except Exception as e:
        return f"Error deleting account: {e}"

    finally:
        conn.close()

    return '''
        <h2>Your account and diary entries have been deleted.</h2>
        <p><a href="/register">Click here to register again</a></p>
    '''


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)