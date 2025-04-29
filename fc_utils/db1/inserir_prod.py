import psycopg2
from config import DB_CONFIG

# Função para inserir início da produção
def inserir_inicio_prod(inicio_prod):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO produção (inicio_prod)
            VALUES (%s)
        """, (inicio_prod,))

        conn.commit()
        cur.close()
        conn.close()
        print("⚙️ [PRODUÇÃO] Início da produção inserido com sucesso!")

    except Exception as e:
        print(f"❌ [PRODUÇÃO] Erro ao inserir início: {e}")

# Função para atualizar o fim da produção
def atualizar_fim_prod(fim_prod):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("""
            UPDATE produção
            SET fim_prod = %s
            WHERE id = (
                SELECT id FROM produção
                WHERE fim_prod IS NULL
                ORDER BY inicio_prod ASC
                LIMIT 1
            )
        """, (fim_prod,))

        conn.commit()
        cur.close()
        conn.close()
        print("✅ [PRODUÇÃO] Fim da produção atualizado com sucesso!")

    except Exception as e:
        print(f"❌ [PRODUÇÃO] Erro ao atualizar fim: {e}")

# Função para verificar se existe produção em andamento
def existe_producao_em_andamento():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("""
            SELECT 1 FROM produção
            WHERE fim_prod IS NULL
            LIMIT 1
        """)

        resultado = cur.fetchone()

        cur.close()
        conn.close()

        return resultado is not None

    except Exception as e:
        print(f"❌ [PRODUÇÃO] Erro ao verificar produção em andamento: {e}")
        return False
