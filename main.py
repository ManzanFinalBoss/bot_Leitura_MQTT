from fc_utils.py.iniciar_bots import iniciar_bots
import time

def manter_execucao():
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Encerrado pelo usuário.")


def main():
    iniciar_bots()
    manter_execucao()


if __name__ == "__main__":
    main()
