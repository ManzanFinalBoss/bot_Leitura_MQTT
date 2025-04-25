from datetime import datetime
from fc_utils.db.inserir_falha import inserir_falha

# Variável temporária para armazenar o início da falha
inicio_falha = None

def monitorar_falha(dados):
    global inicio_falha

    # Detecta o início da falha (só registra se ainda não houver valor)
    if "InicioFalha" in dados and dados["InicioFalha"] and not inicio_falha:
        inicio_falha = datetime.now()
        print(f"\n⚠️ Início da falha registrado: {inicio_falha}")

    # Detecta o fim da falha (só registra se houver início já salvo)
    elif "FimFalha" in dados and dados["FimFalha"] and inicio_falha:
        fim_falha = datetime.now()
        tempo_falha = fim_falha - inicio_falha

        # Insere os dados no banco
        inserir_falha(inicio_falha, fim_falha, tempo_falha)

        # Limpa para a próxima falha
        inicio_falha = None
