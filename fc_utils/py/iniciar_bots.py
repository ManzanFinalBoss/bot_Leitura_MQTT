from fc_utils.bots import bot_topico1
# from fc_utils.bots import bot_topico2
from config import MQTT_CONFIG


def iniciar_bot_1():
    bot_topico1.iniciar_bot(
        broker=MQTT_CONFIG['broker'],
        port=MQTT_CONFIG['port'],
        topic=MQTT_CONFIG['topics'][0]
    )

  ##def iniciar_bot_2():
    # bot_topico2.iniciar_bot(
    #     broker=MQTT_CONFIG['broker'],
    #     port=MQTT_CONFIG['port'],
    #     topic=MQTT_CONFIG['topics'][1]
    # )

def iniciar_bots():
    print("🤖 Iniciando bots de leitura MQTT...\n")
    iniciar_bot_1()
    #iniciar_bot_2()
    print("\n💤 Bots rodando... pressione Ctrl+C para encerrar.")
