import psycopg2
from config import DB_CONFIG
from datetime import datetime
from zoneinfo import ZoneInfo

def inserir_consumo(consumo_ar, consumo_energia, horario=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        if horario is None:
            horario = datetime.now(ZoneInfo("America/Sao_Paulo"))

        # Garantir que o horário está com fuso de SP explicitamente
        if horario.tzinfo is None:
            horario = horario.replace(tzinfo=ZoneInfo("America/Sao_Paulo"))

        cur.execute("""
            INSERT INTO consumo (horario, consumo_ar, consumo_energia)
            VALUES (%s, %s, %s)
        """, (horario, consumo_ar, consumo_energia))

        conn.commit()
        cur.close()
        conn.close()
        print(f"💧 [CONSUMO] Dados inseridos com sucesso! Horário registrado: {horario}")

    except Exception as e:
        print(f"❌ [CONSUMO] Erro ao inserir dados: {e}")
