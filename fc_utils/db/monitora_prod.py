from datetime import datetime
from fc_utils.db.inserir_prod import inserir_prod

# Variável temporária para armazenar o início da produção
inicio_prod = None

def monitorar_prod(dados):
    global inicio_prod

    # Detecta o início da produção (só registra se ainda não houver valor)
    if "InicioProd" in dados and dados["InicioProd"] and not inicio_prod:
        inicio_prod = datetime.now()
        print(f"\n⚙️ Início da produção registrado: {inicio_prod}")

    # Detecta o fim da produção (só registra se houver início já salvo)
    elif "FimProd" in dados and dados["FimProd"] and inicio_prod:
        fim_prod = datetime.now()
        tempo_producao = fim_prod - inicio_prod

        # Insere os dados no banco
        inserir_prod(inicio_prod, fim_prod, tempo_producao)

        # Limpa para a próxima produção
        inicio_prod = None
