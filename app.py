from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Variáveis de controle
historico = []
sinais = []
bot_ativo = False
stop_win = 0
stop_loss = 0
wins = 0
losses = 0

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        conta = request.form['conta']
        session['email'] = email
        session['senha'] = senha
        session['conta'] = conta
        return redirect(url_for('painel'))
    return render_template('login.html')

@app.route('/painel', methods=['GET', 'POST'])
def painel():
    global stop_win, stop_loss
    if request.method == 'POST':
        stop_win = int(request.form['stop_win'])
        stop_loss = int(request.form['stop_loss'])

        file = request.files['arquivo']
        if file:
            conteudo = file.read().decode('utf-8')
            for linha in conteudo.strip().split('\n'):
                if linha.count(';') == 3:
                    sinais.append(linha.strip())
        return redirect(url_for('painel'))

    return render_template('index.html', historico=historico, stop_win=stop_win, stop_loss=stop_loss)


@app.route('/start-bot', methods=['POST'])
def start_bot():
    global bot_ativo, wins, losses
    bot_ativo = True
    wins = 0
    losses = 0
    executar_bot()
    return redirect(url_for('painel'))

@app.route('/stop-bot', methods=['POST'])
def stop_bot():
    global bot_ativo
    bot_ativo = False
    return redirect(url_for('painel'))

def executar_bot():
    import threading
    import time
    from playsound import playsound

    def rodar():
        global sinais, wins, losses, bot_ativo
        while bot_ativo and sinais:
            sinal = sinais.pop(0)
            tf, par, hora, direcao = sinal.split(';')

            agora = datetime.now().strftime('%H:%M')
            if hora == agora:
                resultado = 'WIN' if (wins - losses) % 2 == 0 else 'LOSS'
                if resultado == 'WIN':
                    wins += 1
                else:
                    losses += 1
                historico.append({
                    'horario': agora,
                    'par': par,
                    'direcao': direcao,
                    'resultado': resultado
                })
                try:
                    playsound('static/beep.mp3')
                except:
                    pass
                if wins >= stop_win or losses >= stop_loss:
                    break
            time.sleep(30)
        bot_ativo = False

    threading.Thread(target=rodar).start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
