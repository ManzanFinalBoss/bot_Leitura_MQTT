import psycopg2
from config import DB_CONFIG
from datetime import datetime

def inserir_consumo(consumo_ar, consumo_energia, horario=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        if horario is None:
            horario = datetime.now()

        cur.execute("""
            INSERT INTO consumo (horario, consumo_ar, consumo_energia)
            VALUES (%s, %s, %s)
        """, (horario, consumo_ar, consumo_energia))

        conn.commit()
        cur.close()
        conn.close()
        print("💧 [CONSUMO] Dados inseridos com sucesso!")

    except Exception as e:
        print(f"❌ [CONSUMO] Erro ao inserir dados: {e}")
