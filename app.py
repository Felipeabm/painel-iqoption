from iq_connect import executar_sinais

from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Rota de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        conta = request.form.get('conta')  # demo ou real

        if usuario and senha:
            session['usuario'] = usuario
            session['conta'] = conta
            return redirect(url_for('painel'))
        else:
            flash('Usuário ou senha inválidos.')

    return render_template('login.html')


# Rota do painel
@app.route('/painel', methods=['GET'])
def painel():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


# Rota para iniciar o bot
@app.route('/iniciar-bot', methods=['POST'])
def iniciar_bot():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    arquivo = request.files.get('arquivo')
    valor = request.form.get('valor')
    stop_win = request.form.get('stop_win')
    stop_loss = request.form.get('stop_loss')

    if not arquivo or not valor or not stop_win or not stop_loss:
        return "Preencha todos os campos!", 400
# Executar os sinais
usuario = session['usuario']
conta = session.get('conta', 'demo')  # padrão demo

resposta = executar_sinais(usuario, senha="senha_aqui", conta=conta, sinais=sinais, valor=float(valor))
print(resposta)

    
    # Salvar arquivo no servidor
    caminho = os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename)
    arquivo.save(caminho)

    # Ler conteúdo do arquivo .txt
    try:
        with open(caminho, 'r') as f:
            sinais = f.readlines()
    except Exception as e:
        return f"Erro ao ler o arquivo: {str(e)}", 500

    # Aqui começaria a lógica do bot (conectando com IQ Option, etc)
    print("Bot iniciado com os seguintes parâmetros:")
    print(f"Valor: {valor}")
    print(f"Stop Win: {stop_win}")
    print(f"Stop Loss: {stop_loss}")
    print(f"Total de sinais carregados: {len(sinais)}")

    return "Bot iniciado com sucesso!"


# Rota para parar o bot (futura implementação)
@app.route('/parar-bot', methods=['POST'])
def parar_bot():
    print("Bot foi parado manualmente.")
    return "Bot parado com sucesso!"


# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render define a porta por variável de ambiente
    app.run(host='0.0.0.0', port=port)

