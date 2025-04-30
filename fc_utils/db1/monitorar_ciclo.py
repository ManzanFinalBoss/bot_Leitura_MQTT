from datetime import datetime
from zoneinfo import ZoneInfo
from fc_utils.db1.inserir_ciclo import (
    inserir_inicio_ciclo,
    atualizar_fim_ciclo,
    atualizar_qualidade_ciclo,
    existe_ciclo_em_andamento
)

# Variável para controle local (não precisa mais guardar tudo)
inicio_ciclo_local = None

def monitorar_ciclo(dados):
    global inicio_ciclo_local

    # Detecta início do ciclo (bCiclo = True)
    if dados.get("bCiclo") is True:
        if not existe_ciclo_em_andamento():
            inicio_ciclo_local = datetime.now(ZoneInfo("America/Sao_Paulo"))
            inserir_inicio_ciclo(inicio_ciclo_local)
            print(f"\n⏰ Início do ciclo registrado: {inicio_ciclo_local}")
        else:
            print("\n⚠️ Sinal de início ignorado: já existe ciclo em andamento.")

    # Detecta fim do ciclo (bCiclo = False)
    elif dados.get("bCiclo") is False:
        if existe_ciclo_em_andamento():
            fim_ciclo = datetime.now(ZoneInfo("America/Sao_Paulo"))
            atualizar_fim_ciclo(fim_ciclo)
            print(f"🛑 Fim do ciclo registrado: {fim_ciclo}")
        else:
            print("\n⚠️ Sinal de fim ignorado: nenhum ciclo em andamento.")

        inicio_ciclo_local = None

    # Detecta e atualiza qualidade
    if "bPecasDefeito" in dados:
        valor_recebido = dados["bPecasDefeito"]
        print(f"📥 Valor bruto recebido para bPecasDefeito: {valor_recebido}")

        if isinstance(valor_recebido, bool) and valor_recebido is True:
            sucesso = atualizar_qualidade_ciclo(0)  # 0 = peça defeituosa
            if sucesso:
                print(f"🎯 Qualidade atualizada (defeito)")

    if "bPecasOK" in dados:
        valor_recebido = dados["bPecasOK"]
        print(f"📥 Valor bruto recebido para bPecasOK: {valor_recebido}")

        if isinstance(valor_recebido, bool) and valor_recebido is True:
            sucesso = atualizar_qualidade_ciclo(1)  # 1 = peça OK
            if sucesso:
                print(f"🎯 Qualidade atualizada (OK)")
