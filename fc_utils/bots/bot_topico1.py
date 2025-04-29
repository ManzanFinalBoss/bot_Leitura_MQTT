import paho.mqtt.client as mqtt
from fc_utils.py.on_connect import gerar_on_connect
from fc_utils.py.on_message import gerar_on_message
from fc_utils.db1.criar_tabela_consumo import criar_tabela_consumo
from fc_utils.db1.criar_tabela_falhas import criar_tabela_falhas
from fc_utils.db1.criar_tabela_produção import criar_tabela_produção
from fc_utils.db1.criar_tabela_ciclo import criar_tabela_ciclo
from fc_utils.db1.criar_tabela_oee import criar_tabela_oee


def iniciar_bot(broker, port, topic):
    nome_bot = "topico1"

    print(f"🔌 [{nome_bot}] Conectando ao broker {broker}:{port} no tópico '{topic}'...")
    client = mqtt.Client(userdata={"topic": topic})
    client.on_connect = gerar_on_connect(nome_bot)
    client.on_message = gerar_on_message(nome_bot)
    client.connect(broker, port, 60)
    client.loop_start()
    criar_tabela_produção()
    criar_tabela_ciclo()
    criar_tabela_consumo()
    criar_tabela_falhas()
    criar_tabela_oee()

 
