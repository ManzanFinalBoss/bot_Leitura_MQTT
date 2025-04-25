from datetime import datetime
from fc_utils.db.inserir_ciclo import inserir_ciclo

# Variáveis temporárias para armazenar dados entre mensagens
inicio_ciclo = None
fim_ciclo = None
tempo_total = None
qualidade = None

def monitorar_ciclo(dados):
    global inicio_ciclo, fim_ciclo, tempo_total, qualidade

    # Detecta início do ciclo (bCiclo = True)
    if "bCiclo" in dados and dados["bCiclo"] is True and not inicio_ciclo:
        inicio_ciclo = datetime.now()
        print(f"\n⏰ Início do ciclo registrado: {inicio_ciclo}")

    # Detecta fim do ciclo (bCiclo = False)
    elif "bCiclo" in dados and dados["bCiclo"] is False and inicio_ciclo and not fim_ciclo:
        fim_ciclo = datetime.now()
        tempo_total = (fim_ciclo - inicio_ciclo).total_seconds()
        print(f"🛑 Fim do ciclo registrado: {fim_ciclo} | Tempo Total: {tempo_total:.2f}s")

    # Detecta e armazena qualidade (usando bPecasDefeito)
    if "bPecasDefeito" in dados:
        valor_recebido = dados["bPecasDefeito"]
        print(f"📥 Valor bruto recebido para bPecasDefeito: {valor_recebido}")

        if isinstance(valor_recebido, bool):
            qualidade = 0 if valor_recebido else 1
            print(f"🎯 Qualidade registrada (convertido): {qualidade}")
        else:
            print(f"⚠️ Valor inválido para bPecasDefeito: {valor_recebido}")

    # Verifica se já tem todos os dados para inserir no banco
    if inicio_ciclo and fim_ciclo and qualidade is not None:
        inserir_ciclo(inicio_ciclo, fim_ciclo, tempo_total, qualidade)
        print(f"✅ Ciclo completo registrado no banco! Tempo: {tempo_total:.2f}s | Qualidade: {qualidade}")

        # Reseta as variáveis para o próximo ciclo
        inicio_ciclo = None
        fim_ciclo = None
        tempo_total = None
        qualidade = None
