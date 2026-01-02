import os
import sqlite3
import subprocess
import pickle
from flask import Flask, request, render_template_string

app = Flask(__name__)

app.secret_key = "super_secret_password_123"

DEBUG_MODE = True

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return "Vulnerable App is Running"

@app.route('/search')
def search_user():
    username = request.args.get('username')

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query) 
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return f"Found user: {user['username']}"
    return "User not found"

@app.route('/ping')
def ping_host():
    hostname = request.args.get('hostname')

    command = "ping -c 1 " + hostname
    os.system(command)
    
    return f"Pinged {hostname}"

@app.route('/hello')
def hello():
    name = request.args.get('name')

    template = f"<h1>Hello {name}</h1>"
    return render_template_string(template)

@app.route('/load_config', methods=['POST'])
def load_config():
    data = request.data

    config = pickle.loads(data)
    
    return f"Config loaded: {config}"

if __name__ == '__main__':

    app.run(debug=DEBUG_MODE, host='0.0.0.0', port=5000)
