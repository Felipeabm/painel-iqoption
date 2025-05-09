try:
    from iqoptionapi.api import IQ_Option
except ImportError:
    from iqoptionapi.stable_api import IQ_Option

import time

def executar_sinais(email, senha, conta, sinais, valor):
    Iq = IQ_Option(email, senha)
    Iq.connect()

    if conta == "demo":
        Iq.change_balance("practice")
    else:
        Iq.change_balance("REAL")

    if not Iq.check_connect():
        return "Erro ao conectar na IQ Option."

    for linha in sinais:
        if not linha.strip():
            continue
        try:
            horario, par, direcao, timeframe = linha.strip().split(';')
            timeframe = int(timeframe)

            # Esperar até o horário do sinal
            while True:
                agora = time.strftime('%H:%M')
                if agora == horario:
                    break
                time.sleep(1)

            print(f"Executando sinal: {par} - {direcao} - {timeframe} - {valor}")
            status, id = Iq.buy(valor, par, direcao, timeframe)
            print(f"Entrada executada? {status} - ID: {id}")

        except Exception as e:
            print(f"Erro ao executar sinal: {linha} - {e}")
