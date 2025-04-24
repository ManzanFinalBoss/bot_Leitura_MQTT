def gerar_on_connect(bot_name):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"✅ [{bot_name}] Conectado com sucesso ao broker!")
            client.subscribe(userdata['topic'])
            print(f"📡 [{bot_name}] Subscrito no tópico '{userdata['topic']}'")
        else:
            print(f"❌ [{bot_name}] Falha na conexão. Código: {rc}")
    return on_connect
