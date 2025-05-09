from flask import Flask, render_template, request, redirect, url_for, session, flash
from iq_connect import executar_sinais

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Altere para uma chave segura

@app.route('/')
def login():
    return render_template('login_iq.html')

@app.route('/login', methods=['POST'])
def fazer_login():
    email = request.form['email']
    senha = request.form['senha']
    
    if email and senha:
        session['email'] = email
        session['senha'] = senha
        return redirect(url_for('painel'))
    else:
        flash('E-mail ou senha inválidos.', 'danger')
        return redirect(url_for('login'))

@app.route('/painel')
def painel():
    if 'email' in session:
        return render_template('painel.html')
    else:
        return redirect(url_for('login'))

@app.route('/iniciar-bot', methods=['GET'])
def iniciar_bot():
    if 'email' in session and 'senha' in session:
        try:
            executar_sinais(session['email'], session['senha'])
            flash("Bot iniciado com sucesso!", "success")
        except Exception as e:
            print(f"[ERRO] Falha ao iniciar o bot: {e}")
            flash("Erro ao iniciar o bot. Verifique o terminal.", "danger")
        return redirect(url_for('painel'))
    else:
        flash("Você precisa estar logado para iniciar o bot.", "warning")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
