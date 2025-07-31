from flask import Flask, render_template, request, redirect, session
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATA_FILE = 'database.json'
USERNAME = os.getenv("PANEL_USER")
PASSWORD = os.getenv("PANEL_PASS")

def read_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('logged_in'):
        return redirect('/')
    
    data = read_data()

    if request.method == 'POST':
        data['mensagem'] = request.form['mensagem']
        data['tempo_envio'] = int(request.form['tempo_envio'])
        data['validade'] = int(request.form['validade'])
        data['estrategia'] = request.form['estrategia']
        data['bot_ativo'] = 'bot_ativo' in request.form
        write_data(data)
    
    return render_template('index.html', data=data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
