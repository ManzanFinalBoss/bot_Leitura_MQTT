import paho.mqtt.client as mqtt
from fc_utils.py.on_connect import gerar_on_connect
from fc_utils.py.on_message import gerar_on_message

def iniciar_bot(broker, port, topic):
    nome_bot = "topico1"

    print(f"🔌 [{nome_bot}] Conectando ao broker {broker}:{port} no tópico '{topic}'...")
    client = mqtt.Client(userdata={"topic": topic})
    client.on_connect = gerar_on_connect(nome_bot)
    client.on_message = gerar_on_message(nome_bot)
    client.connect(broker, port, 60)
    client.loop_start()
