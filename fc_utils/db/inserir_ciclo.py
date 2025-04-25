import psycopg2
from config import DB_CONFIG

def inserir_ciclo(inicio, fim, tempo_total, qualidade):
    try:
        # Conecta ao banco
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Executa o INSERT na tabela correta
        cur.execute("""
        INSERT INTO ciclo_pecas (inicio_ciclo, fim_ciclo, qualidade)
        VALUES (%s, %s, %s)
        """, (inicio, fim, qualidade))



        # Confirma e fecha
        conn.commit()
        cur.close()
        conn.close()
        print("✅ [CICLO] Dados inseridos com sucesso!")

    except Exception as e:
        print(f"❌ [CICLO] Erro ao inserir dados: {e}")