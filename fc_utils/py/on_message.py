import json
from fc_utils.db.monitorar_ciclo import monitorar_ciclo
from fc_utils.db.monitorar_falhas import monitorar_falha
from fc_utils.db.monitora_prod import monitorar_prod
from fc_utils.db.monitorar_consumo import monitorar_consumo


def gerar_on_message(bot_name):
    def on_message(client, userdata, msg):
        try:
            payload = msg.payload.decode()
            print(f"\n📩 [{bot_name}] Mensagem recebida: {payload}")

            dados = json.loads(payload)
            print(f"📦 [{bot_name}] Dados tratados:")
            for chave, valor in dados.items():
                print(f"    {chave}: {valor}")
            monitorar_ciclo(dados)  
            monitorar_falha(dados)
            monitorar_prod(dados)
            monitorar_consumo(dados)
        except json.JSONDecodeError:
            print(f"⚠️ [{bot_name}] Erro ao decodificar JSON!")
    return on_message
