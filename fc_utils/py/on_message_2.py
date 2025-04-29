import json
import re
from fc_utils.db1.monitorar_ciclo import monitorar_ciclo
from fc_utils.db1.monitorar_falhas import monitorar_falha
from fc_utils.db1.monitora_prod import monitorar_prod
from fc_utils.db1.monitorar_consumo import monitorar_consumo

# Função para limpar parênteses das chaves
def limpar_chaves(dados):
    novos_dados = {}
    for chave, valor in dados.items():
        chave_limpa = re.sub(r"\s*\([^)]*\)", "", chave).strip()
        novos_dados[chave_limpa] = valor
    return novos_dados

def gerar_on_message(bot_name):
    def on_message(client, userdata, msg):
        payload = msg.payload.decode()
        print(f"\n📩 [{bot_name}] Mensagem recebida: {payload}")

        dados = {}

        # Tenta decodificar como JSON padrão
        try:
            dados = json.loads(payload)
            # Limpar as chaves depois de carregar o JSON
            dados = limpar_chaves(dados)

        except json.JSONDecodeError:
            # Trata como string simples: {bProducao: TRUE}
            if payload.startswith("{") and payload.endswith("}"):
                try:
                    texto_limpo = payload[1:-1]  # remove as chaves
                    chave, valor = texto_limpo.split(":")
                    chave = chave.strip()
                    valor = valor.strip().upper()

                    # Limpa parênteses da chave
                    chave = re.sub(r"\s*\([^)]*\)", "", chave)

                    if valor in ["TRUE", "FALSE"]:
                        valor = True if valor == "TRUE" else False
                    elif valor.isdigit():
                        valor = int(valor)

                    dados[chave] = valor
                except Exception as e:
                    print(f"⚠️ [{bot_name}] Erro ao tratar string simples: {e}")
                    return  # Não processa se não for possível interpretar

        print(f"📦 [{bot_name}] Dados tratados:")
        for chave, valor in dados.items():
            print(f"    {chave}: {valor}")

        # Chama todas as funções de monitoramento
        monitorar_ciclo(dados)
        monitorar_falha(dados)
        monitorar_prod(dados)
        monitorar_consumo(dados)

    return on_message
