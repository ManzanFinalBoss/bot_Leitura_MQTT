from datetime import datetime
from fc_utils.db.inserir_ciclo import inserir_ciclo

# Variáveis temporárias para armazenar dados entre mensagens
inicio_ciclo = None
fim_ciclo = None
qualidade = None

def monitorar_ciclo(dados):
    global inicio_ciclo, fim_ciclo, qualidade

    # Detectou início do ciclo (somente se ainda não houver um valor)
    if "InicioCiclo" in dados and dados["InicioCiclo"] and not inicio_ciclo:
        inicio_ciclo = datetime.now()
        print(f"\n⏰ Início do ciclo registrado: {inicio_ciclo}")

    # Detectou fim do ciclo (somente se ainda não houver um valor)
    if "FimCiclo" in dados and dados["FimCiclo"] and not fim_ciclo:
        fim_ciclo = datetime.now()
        print(f"🔴 Fim do ciclo registrado: {fim_ciclo}")

    # Armazena qualidade, apenas se for 0 ou 1
    if "ControleQualidade" in dados:
        if dados["ControleQualidade"] in [0, 1]:
            qualidade = dados["ControleQualidade"]
            print(f"✅ Controle de qualidade registrado: {qualidade}")
        else:
            print(f"⚠️ Valor inválido para ControleQualidade: {dados['ControleQualidade']} (ignorado)")

    # Só insere se todos os dados estiverem presentes
    if inicio_ciclo and fim_ciclo and qualidade is not None:
        tempo_total = (fim_ciclo - inicio_ciclo).total_seconds()

        inserir_ciclo(inicio_ciclo, fim_ciclo, tempo_total, qualidade)

        # Limpa para o próximo ciclo
        inicio_ciclo = None
        fim_ciclo = None
        qualidade = None
