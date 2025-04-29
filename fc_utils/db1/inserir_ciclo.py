import psycopg2
from config import DB_CONFIG

def inserir_inicio_ciclo(inicio_ciclo):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO ciclo_pecas (inicio_ciclo)
            VALUES (%s)
        """, (inicio_ciclo,))

        conn.commit()
        cur.close()
        conn.close()
        print("⏰ [CICLO] Início do ciclo inserido com sucesso!")

    except Exception as e:
        print(f"❌ [CICLO] Erro ao inserir início: {e}")

def atualizar_fim_ciclo(fim_ciclo):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("""
            WITH cte AS (
                SELECT id
                FROM ciclo_pecas
                WHERE fim_ciclo IS NULL
                ORDER BY inicio_ciclo ASC
                LIMIT 1
            )
            UPDATE ciclo_pecas
            SET fim_ciclo = %s
            WHERE id IN (SELECT id FROM cte)
        """, (fim_ciclo,))

        linhas_afetadas = cur.rowcount

        conn.commit()
        cur.close()
        conn.close()

        if linhas_afetadas > 0:
            print("🛑 [CICLO] Fim do ciclo atualizado com sucesso!")
            return True
        else:
            print("⚠️ [CICLO] Nenhum ciclo aberto para finalizar.")
            return False

    except Exception as e:
        print(f"❌ [CICLO] Erro ao atualizar fim: {e}")
        return False

def atualizar_qualidade_ciclo(qualidade):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("""
            WITH cte AS (
                SELECT id
                FROM ciclo_pecas
                WHERE qualidade IS NULL
                  AND fim_ciclo IS NOT NULL
                ORDER BY inicio_ciclo ASC
                LIMIT 1
            )
            UPDATE ciclo_pecas
            SET qualidade = %s
            WHERE id IN (SELECT id FROM cte)
        """, (qualidade,))

        linhas_afetadas = cur.rowcount

        conn.commit()
        cur.close()
        conn.close()

        if linhas_afetadas > 0:
            print("🎯 [CICLO] Qualidade do ciclo atualizada com sucesso!")
            return True
        else:
            print("⚠️ [CICLO] Nenhum ciclo disponível para atualizar a qualidade.")
            return False

    except Exception as e:
        print(f"❌ [CICLO] Erro ao atualizar qualidade: {e}")
        return False

def existe_ciclo_em_andamento():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("""
            SELECT 1 FROM ciclo_pecas
            WHERE fim_ciclo IS NULL
            LIMIT 1
        """)

        resultado = cur.fetchone()

        cur.close()
        conn.close()

        return resultado is not None

    except Exception as e:
        print(f"❌ [CICLO] Erro ao verificar ciclo em andamento: {e}")
        return False
