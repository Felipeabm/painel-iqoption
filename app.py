from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Simula histórico de entradas
historico_entradas = []

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']
    conta = request.form['conta']
    if email and senha:
        session['usuario'] = email
        session['conta'] = conta
        return redirect(url_for('painel'))
    return redirect(url_for('index'))

@app.route('/painel')
def painel():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'arquivo' not in request.files:
        return 'Nenhum arquivo enviado', 400
    file = request.files['arquivo']
    if file.filename == '':
        return 'Nome de arquivo vazio', 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    session['arquivo'] = filepath
    return 'Arquivo enviado com sucesso'

@app.route('/iniciar', methods=['POST'])
def iniciar():
    try:
        entrada = request.form['entrada']
        stop_win = request.form['stop_win']
        stop_loss = request.form['stop_loss']
        arquivo = session.get('arquivo')

        if not all([entrada, stop_win, stop_loss, arquivo]):
            return "Dados incompletos para iniciar o bot", 400

        # Simulação da lógica de bot e registro no histórico
        historico_entradas.append({
            "data": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "status": "Bot Iniciado",
            "arquivo": os.path.basename(arquivo)
        })
        return jsonify({"mensagem": "Bot iniciado com sucesso"})
    except Exception as e:
        return f"Erro interno: {str(e)}", 500

@app.route('/historico')
def historico():
    return jsonify(historico_entradas)

@app.route('/limpar', methods=['POST'])
def limpar():
    session.pop('arquivo', None)
    return 'Limpo com sucesso'

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Arquivo de áudio
@app.route('/audio/<filename>')
def audio(filename):
    return send_from_directory('static/audio', filename)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
