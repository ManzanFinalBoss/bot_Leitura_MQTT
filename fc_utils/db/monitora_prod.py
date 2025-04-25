from datetime import datetime
from fc_utils.db.inserir_prod import inserir_prod

# Variável temporária para armazenar o início da produção
inicio_prod = None

def monitorar_prod(dados):
    global inicio_prod

    # Detecta início da produção (bProducao = True) e ainda não registrado
    if "bProducao" in dados and dados["bProducao"] is True and not inicio_prod:
        inicio_prod = datetime.now()
        print(f"\n⚙️ Início da produção registrado: {inicio_prod}")

    # Detecta fim da produção (bProducao = False) e início já registrado
    elif "bProducao" in dados and dados["bProducao"] is False and inicio_prod:
        fim_prod = datetime.now()
        tempo_producao = fim_prod - inicio_prod

        inserir_prod(inicio_prod, fim_prod, tempo_producao)

        print(f"✅ Produção finalizada! Tempo total: {tempo_producao}")
        
        # Reseta para próxima produção
        inicio_prod = None
