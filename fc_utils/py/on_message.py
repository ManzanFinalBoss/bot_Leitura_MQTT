import json
from fc_utils.db.monitorar_producao import monitorar_producao  # ⬅️ Adicione essa linha

def gerar_on_message(bot_name):
    def on_message(client, userdata, msg):
        try:
            payload = msg.payload.decode()
            print(f"\n📩 [{bot_name}] Mensagem recebida: {payload}")

            dados = json.loads(payload)
            print(f"📦 [{bot_name}] Dados tratados:")
            for chave, valor in dados.items():
                print(f"    {chave}: {valor}")

            # 🧠 Nova etapa: processar os dados
            monitorar_producao(dados)  # ⬅️ Aqui a mágica acontece

        except json.JSONDecodeError:
            print(f"⚠️ [{bot_name}] Erro ao decodificar JSON!")
    return on_message
