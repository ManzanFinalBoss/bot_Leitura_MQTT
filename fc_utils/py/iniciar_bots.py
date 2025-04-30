from fc_utils.bots import bot_topico1
from config import MQTT_CONFIG


def iniciar_bot_1():
    bot_topico1.iniciar_bot(
        broker=MQTT_CONFIG['broker'],
        port=MQTT_CONFIG['port'],
        topic=MQTT_CONFIG['topics'][0]
    )


def iniciar_bots():
    print("🤖 Iniciando bots de leitura MQTT...\n")
    iniciar_bot_1()
    print("\n💤 Bots rodando... pressione Ctrl+C para encerrar.")
