import time
from iqoptionapi.stable_api import IQ_Option

def executar_sinais(email, senha):
    print("Iniciando login na IQ Option...")
    API = IQ_Option(email, senha)
    API.connect()

    if not API.check_connect():
        print("Erro ao conectar com a IQ Option. Verifique seu e-mail/senha.")
        return

    print("Conectado com sucesso!")

    try:
        with open("sinais.txt", "r") as arquivo:
            sinais = arquivo.readlines()
    except FileNotFoundError:
        print("Arquivo 'sinais.txt' não encontrado. Nenhum sinal foi executado.")
        return

    for linha in sinais:
        try:
            tempo, par, horario, direcao = linha.strip().split(";")
            print(f"Aguardando horário {horario} para entrar no par {par} ({direcao})...")

            while True:
                agora = time.strftime("%H:%M")
                if agora == horario:
                    duracao = int(tempo.replace("M", ""))  # Ex: "M1" -> 1
                    valor = 2  # valor fixo; pode ser parametrizado depois
                    entrada = API.buy(valor, par, direcao.lower(), duracao)

                    if entrada[0]:
                        print(f"✅ Entrada realizada: {par} | Direção: {direcao} | Expiração: {tempo}")
                    else:
                        print(f"❌ Erro ao realizar entrada: {par}")

                    break
                time.sleep(1)

        except ValueError:
            print(f"Formato de linha inválido: {linha}")
            continue

    API.disconnect()
    print("Bot finalizado.")
