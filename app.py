from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')
    conta = request.form.get('conta')

    if email and senha and conta:
        session['email'] = email
        session['senha'] = senha
        session['conta'] = conta
        return redirect(url_for('painel'))
    else:
        return redirect(url_for('index'))

@app.route('/painel')
def painel():
    if 'email' in session:
        return render_template('painel.html',
                               email=session['email'],
                               conta=session['conta'])
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
