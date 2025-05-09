# iq_connect.py

from iqoptionapi.api import IQ_Option
import time
from datetime import datetime

def conectar(email, senha):
    Iq = IQ_Option(email, senha)
    Iq.connect()
    if Iq.check_connect():
        print("✅ Conectado com sucesso na IQ Option!")
        return Iq
    else:
        print("❌ Falha ao conectar na IQ Option.")
        return None

def executar_sinais(email, senha):
    Iq = conectar(email, senha)
    if not Iq:
        return

    Iq.change_balance("PRACTICE")  # Use "REAL" se for conta real

    try:
        with open("sinais.txt", "r") as f:
            sinais = [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        print("❌ Arquivo 'sinais.txt' não encontrado.")
        return

    print("🕒 Aguardando sinais...")

    while sinais:
        agora = datetime.now().strftime("%H:%M")
        for sinal in sinais[:]:
            partes = sinal.split()
            if len(partes) < 3:
                continue
            horario, par, direcao = partes
            if horario == agora:
                print(f"⏰ {horario} | Executando entrada: {par} - {direcao.upper()}")
                status, id = Iq.buy(2, par, direcao.lower(), 1)
                if status:
                    print(f"✅ Entrada realizada com sucesso! ID: {id}")
                else:
                    print("❌ Falha ao realizar a entrada.")
                sinais.remove(sinal)
        time.sleep(1)
