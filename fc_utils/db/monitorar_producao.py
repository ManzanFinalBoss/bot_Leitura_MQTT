from datetime import datetime
from fc_utils.db.inserir_producao import inserir_producao

# Variáveis temporárias para armazenar dados entre mensagens
inicio_prod = None
fim_prod = None
qualidade = None

def monitorar_producao(dados):
    global inicio_prod, fim_prod, qualidade

    # Detectou início da produção (somente se ainda não houver um valor)
    if "InicioProd" in dados and dados["InicioProd"] and not inicio_prod:
        inicio_prod = datetime.now()
        print(f"\n⏰ Início da produção registrado: {inicio_prod}")

    # Detectou fim da produção (somente se ainda não houver um valor)
    if "FimProd" in dados and dados["FimProd"] and not fim_prod:
        fim_prod = datetime.now()
        print(f"🔴 Fim da produção registrado: {fim_prod}")

    # Armazena qualidade (mesmo que venha antes do fim)
    if "ControleQualidade" in dados:
        qualidade = dados["ControleQualidade"]

    # Só insere se todos os dados estiverem presentes
    if inicio_prod and fim_prod and qualidade is not None:
        tempo_total = (fim_prod - inicio_prod).total_seconds()

        inserir_producao(inicio_prod, fim_prod, tempo_total, qualidade)

        # Limpa para próxima produção
        inicio_prod = None
        fim_prod = None
        qualidade = None
