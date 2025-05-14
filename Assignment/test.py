import pyodbc
from flask import Flask

app = Flask(__name__)

conn = pyodbc.connect(
    'DRIVER={testing};'
    'SERVER=192.168.50.101;'
    'DATABASE=EncryptedDB;'
)

@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"