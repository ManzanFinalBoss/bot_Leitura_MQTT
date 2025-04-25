import psycopg2
from config import DB_CONFIG

def inserir_falha(inicio_falha, fim_falha, tempo_falha):
    try:
        # Conecta ao banco
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Executa o INSERT
        cur.execute("""
            INSERT INTO falhas (inicio_falha, fim_falha)
            VALUES (%s, %s)
        """, (inicio_falha, fim_falha))

        # Confirma e fecha
        conn.commit()
        cur.close()
        conn.close()
        print("⚠️ [FALHA] Dados de falha inseridos com sucesso!")

    except Exception as e:
        print(f"❌ [FALHA] Erro ao inserir dados: {e}")
