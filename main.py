#importa os bots
from bots import bot_topico1
#from bots import bot_topico2
import time
#importa as configurações feitas no config.py
from config import MQTT_CONFIG             

#Definindo uma função 
def main():
    print("🤖 Iniciando bots de leitura MQTT...\n")

    ## 🔽 BOT 1
    bot_topico1.iniciar_bot(
        broker=MQTT_CONFIG['broker'],         #importa o broker das configs
        port=MQTT_CONFIG['port'],             #importa a port das configs
        topic=MQTT_CONFIG['topics'][0]        #importa o tópico das configs [n] é o tópico desejado, começando em 0
    )

    ## 🔽 BOT 2
    #bot_topico2.iniciar_bot(
    #    broker=MQTT_CONFIG['broker'],         #importa o broker das configs      
    #    port=MQTT_CONFIG['port'],             #importa a port das configs
    #    topic=MQTT_CONFIG['topics'][1]        #importa o tópico das configs [n] é o tópico desejado, começando em 0
    # )

    print("\n💤 Bots rodando... pressione Ctrl+C para encerrar.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:  #ctrl + C
        print("\n🛑 Encerrado pelo usuário.")


#Executa a função main() se, e somente se, ela foi iniciada diretamente
if __name__ == "__main__":
    main()