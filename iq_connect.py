import os
from iqoptionapi.stable_api import IQ_Option
import time

def executar_sinais(email, senha):
    print(f"[INFO] Conectando com {email}...")
    Iq = IQ_Option(email, senha)
    Iq.connect()

    if not Iq.check_connect():
        print("[ERRO] Falha ao conectar com a IQ Option.")
        return

    print("[OK] Conectado com sucesso.")

    if not os.path.exists("sinais.txt"):
        print("[ERRO] Arquivo sinais.txt não encontrado.")
        return

    with open("sinais.txt", "r") as arquivo:
        sinais = arquivo.readlines()

    for sinal in sinais:
        try:
            tempo, par, horario, direcao = sinal.strip().split(';')
            print(f"[SINAL] Timeframe: {tempo} | Par: {par} | Horário: {horario} | Direção: {direcao}")
            # Aqui você pode adicionar lógica real de entrada
        except Exception as e:
            print(f"[ERRO] Falha ao interpretar sinal: {sinal} -> {e}")
    
    print("[INFO] Execução de sinais concluída.")
