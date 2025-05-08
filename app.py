
from flask import Flask, render_template, request, redirect, url_for, session
from iq_connect import iniciar_bot
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

historico = []

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/painel', methods=['POST'])
def painel():
    email = request.form['email']
    senha = request.form['senha']
    session['email'] = email
    session['senha'] = senha
    return render_template('index.html', historico=historico)

@app.route('/iniciar_bot', methods=['POST'])
def iniciar():
    file = request.files['arquivo']
    stop_win = int(request.form['stop_win'])
    stop_loss = int(request.form['stop_loss'])

    if file:
        caminho = os.path.join("sinais.txt")
        file.save(caminho)
        resultado = iniciar_bot(caminho, session['email'], session['senha'], stop_win, stop_loss, historico)
        return redirect(url_for('painel'))

    return redirect(url_for('painel'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
