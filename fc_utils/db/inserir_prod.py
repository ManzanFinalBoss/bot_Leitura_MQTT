import psycopg2
from config import DB_CONFIG

def inserir_prod(inicio_prod, fim_prod, tempo_prod):
    try:
        # Conecta ao banco
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Executa o INSERT
        cur.execute("""
            INSERT INTO produção (inicio_prod, fim_prod)
            VALUES (%s, %s)
        """, (inicio_prod, fim_prod))

        # Confirma e fecha
        conn.commit()
        cur.close()
        conn.close()
        print("⚙️ [PRODUÇÃO] Dados de produção inseridos com sucesso!")

    except Exception as e:
        print(f"❌ [PRODUÇÃO] Erro ao inserir dados: {e}")
