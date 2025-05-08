from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'chave_secreta'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/painel', methods=['POST'])
def painel():
    email = request.form.get('email')
    senha = request.form.get('senha')
    conta = request.form.get('conta')
    session['email'] = email
    session['conta'] = conta
    return render_template('index.html')

@app.route('/iniciar', methods=['POST'])
def iniciar_bot():
    # Aqui vai o processamento do bot com sinais
    try:
        arquivo = request.files['arquivo']
        stop_win = request.form.get('stop_win')
        stop_loss = request.form.get('stop_loss')
        valor_entrada = request.form.get('valor_entrada')
        # Simula execução
        print(f'Arquivo: {arquivo.filename}, Win: {stop_win}, Loss: {stop_loss}, Entrada: {valor_entrada}')
        return 'Bot iniciado!'
    except Exception as e:
        return f'Erro ao iniciar bot: {str(e)}', 500

@app.route('/parar', methods=['POST'])
def parar_bot():
    return 'Bot parado!'

if __name__ == '__main__':
    app.run(debug=True)
