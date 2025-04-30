from datetime import datetime
from zoneinfo import ZoneInfo
from fc_utils.db1.inserir_prod import inserir_inicio_prod, atualizar_fim_prod, existe_producao_em_andamento

inicio_prod = None

def monitorar_prod(dados):
    global inicio_prod

    # Detecta início da produção (bProducao = True)
    if "bProducao" in dados and dados["bProducao"] is True:
        if not existe_producao_em_andamento():
            inicio_prod = datetime.now(ZoneInfo("America/Sao_Paulo"))
            inserir_inicio_prod(inicio_prod)
            print(f"\n⚙️ Início da produção registrado: {inicio_prod}")
        else:
            print("\n⚠️ Sinal de início ignorado: já existe produção em andamento.")

    # Detecta fim da produção (bProducao = False)
    elif "bProducao" in dados and dados["bProducao"] is False:
        if existe_producao_em_andamento():
            fim_prod = datetime.now(ZoneInfo("America/Sao_Paulo"))
            atualizar_fim_prod(fim_prod)
            print(f"✅ Produção finalizada! Fim: {fim_prod}")
        else:
            print("\n⚠️ Sinal de fim ignorado: nenhuma produção em andamento.")
        
        inicio_prod = None
