from fc_utils.py.iniciar_bots import iniciar_bots
from calcular_oee import agendar_oee_diario  # ✅ Importa o agendamento do OEE
import time

def manter_execucao():
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Encerrado pelo usuário.")

def main():
    iniciar_bots()
    agendar_oee_diario()  # ✅ Começa o agendamento do OEE em paralelo
    manter_execucao()

if __name__ == "__main__":
    main()
