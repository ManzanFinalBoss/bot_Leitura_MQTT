from fc_utils.py.iniciar_bots import iniciar_bots
from fc_utils.db.criar_tabela_producao import criar_tabela_producao
from fc_utils.db.criar_tabela_consumo import criar_tabela_consumo
from fc_utils.db.criar_tabela_falhas import criar_tabela_falhas
import time

def manter_execucao():
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Encerrado pelo usuário.")


def main():
    criar_tabela_producao()
    criar_tabela_consumo()
    criar_tabela_falhas()
    iniciar_bots()
    manter_execucao()


if __name__ == "__main__":
    main()
