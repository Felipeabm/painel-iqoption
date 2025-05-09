from iqoptionapi.stable_api import IQ_Option  # Versão funcional estável
import time

def executar_sinais(email, senha):
    print("Iniciando login na IQ Option...")
    Iq = IQ_Option(email, senha)
    Iq.connect()

    if Iq.check_connect():
        print("Login bem-sucedido!")
    else:
        print("Erro ao conectar. Verifique seu email/senha.")
        return

    # Configurações iniciais
    Iq.change_balance("PRACTICE")  # ou "REAL"

    # Leitura dos sinais
    with open("sinais.txt", "r") as arquivo:
        sinais = arquivo.readlines()

    for sinal in sinais:
        dados = sinal.strip().split(",")
        if len(dados) != 3:
            continue

        horario, par, direcao = dados
        print(f"Aguardando para enviar sinal: {horario} | {par} | {direcao}")

        while True:
            hora_atual = time.strftime("%H:%M")
            if hora_atual == horario:
                print(f"Enviando sinal: {par} | {direcao}")
                Iq.buy(2, par, direcao.lower(), 1)  # valor, par, direcao, tempo expiração
                break
            time.sleep(1)
