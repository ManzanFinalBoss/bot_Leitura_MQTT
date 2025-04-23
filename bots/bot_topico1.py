import paho.mqtt.client as mqtt
import json

# Função chamada ao conectar no broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ [topico1] Conectado com sucesso ao broker!")
        client.subscribe(userdata['topic'])
        print(f"📡 [topico1] Subscrito no tópico '{userdata['topic']}'")
    else:
        print(f"❌ [topico1] Falha na conexão. Código: {rc}")

# Função chamada sempre que uma nova mensagem chega
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"\n📩 [topico1] Mensagem recebida: {payload}")

        # Converte JSON em dicionário
        dados = json.loads(payload)

        print("📦 [topico1] Dados tratados:")
        for chave, valor in dados.items():
            print(f"    {chave}: {valor}")

        # TODO: inserir_dados_no_banco(dados)

    except json.JSONDecodeError:
        print("⚠️ [topico1] Erro ao decodificar JSON!")

# Função que inicia o bot
def iniciar_bot(broker, port, topic):
    print(f"🔌 [topico1] Conectando ao broker {broker}:{port} no tópico '{topic}'...")
    client = mqtt.Client(userdata={"topic": topic})
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port, 60)
    client.loop_start()
