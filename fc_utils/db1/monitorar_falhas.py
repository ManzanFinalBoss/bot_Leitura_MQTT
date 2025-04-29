from datetime import datetime
from fc_utils.db1.inserir_falha import inserir_falha

# Variáveis temporárias para armazenar dados entre mensagens
inicio_falha = None
fim_falha = None
tempo_falha = None

def monitorar_falha(dados):
    global inicio_falha, fim_falha, tempo_falha

    # Detecta início da falha (bDetecVazamento = True), se ainda não registrado
    if "bDetecVazamento" in dados and dados["bDetecVazamento"] is True and not inicio_falha:
        inicio_falha = datetime.now()
        print(f"\n⚠️ Início da falha registrado: {inicio_falha}")

    # Detecta fim da falha (bDetecVazamento = False), se houver início já salvo
    elif "bDetecVazamento" in dados and dados["bDetecVazamento"] is False and inicio_falha and not fim_falha:
        fim_falha = datetime.now()
        tempo_falha = fim_falha - inicio_falha
        print(f"🛑 Fim da falha registrado: {fim_falha} | Tempo total da falha: {tempo_falha}")

    # Verifica se já tem início e fim para inserir no banco
    if inicio_falha and fim_falha:
        try:
            inserir_falha(inicio_falha, fim_falha, tempo_falha)
            print(f"✅ Falha completa registrada no banco! Tempo: {tempo_falha}")
        except Exception as e:
            print(f"❌ Erro ao registrar falha no banco: {e}")
        
        # Reseta para a próxima falha
        inicio_falha = None
        fim_falha = None
        tempo_falha = None
