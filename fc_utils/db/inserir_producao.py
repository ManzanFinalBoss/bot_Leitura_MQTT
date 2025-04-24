import psycopg2
from config import DB_CONFIG

def inserir_producao(inicio, fim, tempo_total, qualidade):
    try:
        # Conecta ao banco
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Executa o INSERT na tabela correta
        cur.execute("""
        INSERT INTO producao_pecas (inicio_prod, fim_prod, qualidade)
        VALUES (%s, %s, %s)
        """, (inicio, fim, qualidade))



        # Confirma e fecha
        conn.commit()
        cur.close()
        conn.close()
        print("✅ [PRODUCAO] Dados inseridos com sucesso!")

    except Exception as e:
        print(f"❌ [PRODUCAO] Erro ao inserir dados: {e}")