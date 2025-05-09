# iq_connect.py

try:
    from iqoptionapi.api import IQ_Option  # Versões mais recentes do pacote
except ImportError:
    from iqoptionapi.stable_api import IQ_Option  # Versões antigas do pacote

import time
from datetime import datetime

# Conecta na IQ Option
def conectar(email, senha):
    Iq = IQ_Option(email, senha)
    Iq.connect()
    if Iq.check_connect():
        print("✅ Conectado com sucesso na IQ Option!")
        return Iq
    else:
        print("❌ Falha ao conectar na IQ Option.")
        return None

# Executa os sinais lidos do arquivo sinais.txt
def executar_sinais(email, senha):
    Iq = conectar(email, senha)
    if not Iq:
        return

    Iq.change_balance("PRACTICE")  # ou "REAL"

    with open("sinais.txt", "r") as f:
        sinais = [linha.strip() for linha in f if linha.strip()]

    print("🔄 Aguardando horário dos sinais...")

    while sinais:
        agora = datetime.now().strftime("%H:%M")
        for sinal in sinais[:]:
            partes = sinal.split()
            if len(partes) < 3:
                continue  # sinal mal formatado
            horario, par, direcao = partes
            if horario == agora:
                print(f"📤 Executando sinal das {horario} | Par: {par} | Direção: {direcao.upper()}")
                status, id = Iq.buy(2, par, direcao.lower(), 1)  # Entrada de R$2, expiração M1
                if status:
                    print(f"✅ Entrada realizada com sucesso! ID: {id}")
                else:
                    print("❌ Falha ao realizar a entrada.")
                sinais.remove(sinal)
        time.sleep(1)
