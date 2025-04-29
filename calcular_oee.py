import psycopg2
import schedule
import time
import threading
import os
from dotenv import load_dotenv
from datetime import datetime, time as time_obj
from config import DB_CONFIG

# Carrega .env se existir (não trava se não tiver)
load_dotenv()

def coletar_parametros():
    try:
        data_str = os.getenv("DATA_PRODUCAO")
        horario_inicio_str = os.getenv("HORARIO_INICIO")
        horario_fim_str = os.getenv("HORARIO_FIM")
        tempo_ciclo_ideal_str = os.getenv("TEMPO_CICLO")

        if not all([data_str, horario_inicio_str, horario_fim_str, tempo_ciclo_ideal_str]):
            raise ValueError("Alguma variável de ambiente obrigatória não foi definida!")

        return {
            "data_producao": datetime.strptime(data_str, "%Y-%m-%d").date(),
            "horario_inicio": datetime.strptime(horario_inicio_str, "%H:%M:%S").time(),
            "horario_fim": datetime.strptime(horario_fim_str, "%H:%M:%S").time(),
            "tempo_ciclo_ideal": float(tempo_ciclo_ideal_str)
        }

    except Exception as e:
        print(f"❌ Erro ao coletar parâmetros: {e}")
        exit(1)

def calcular_oee_com_parametros(parametros):
    data_producao = parametros["data_producao"]
    horario_inicio = parametros["horario_inicio"]
    horario_fim = parametros["horario_fim"]
    tempo_ciclo_ideal = parametros["tempo_ciclo_ideal"]

    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                # Tempo produzido real (finalizados + andamento)
                cur.execute("""
                    SELECT 
                        COALESCE(SUM(EXTRACT(EPOCH FROM tempo_prod)), 0)
                        +
                        COALESCE((
                            SELECT EXTRACT(EPOCH FROM (NOW() AT TIME ZONE 'America/Sao_Paulo' - inicio_prod))
                            FROM produção
                            WHERE fim_prod IS NULL AND DATE(inicio_prod) = %s
                            ORDER BY inicio_prod ASC
                            LIMIT 1
                        ), 0)
                    FROM produção
                    WHERE tempo_prod IS NOT NULL AND DATE(inicio_prod) = %s;
                """, (data_producao, data_producao))
                tempo_produzido = float(cur.fetchone()[0] or 0)

                # Contagem de peças boas e totais
                cur.execute("""
                    SELECT 
                        COUNT(*) AS total_pecas,
                        SUM(CASE WHEN qualidade = 1 THEN 1 ELSE 0 END) AS pecas_boas
                    FROM ciclo_pecas
                    WHERE 
                        DATE(inicio_ciclo) = %s
                        AND fim_ciclo IS NOT NULL
                        AND qualidade IS NOT NULL;
                """, (data_producao,))
                total_pecas, pecas_boas = cur.fetchone()
                total_pecas = total_pecas or 0
                pecas_boas = pecas_boas or 0

                # Atualizar tempo programado dinamicamente
                agora = datetime.now().time()
                if agora < horario_fim:
                    tempo_programado_segundos = (
                        datetime.combine(data_producao, agora) -
                        datetime.combine(data_producao, horario_inicio)
                    ).total_seconds()
                else:
                    tempo_programado_segundos = (
                        datetime.combine(data_producao, horario_fim) -
                        datetime.combine(data_producao, horario_inicio)
                    ).total_seconds()

                # Cálculos
                pecas_teoricas = tempo_produzido / tempo_ciclo_ideal if tempo_ciclo_ideal > 0 else 0
                disponibilidade = tempo_produzido / tempo_programado_segundos if tempo_programado_segundos > 0 else 0
                performance = total_pecas / pecas_teoricas if pecas_teoricas > 0 else 0
                qualidade = pecas_boas / total_pecas if total_pecas > 0 else 0
                oee = disponibilidade * performance * qualidade

                # Inserção no banco
                cur.execute("""
                    INSERT INTO oee_diario (
                        data_producao, horario_inicio, horario_fim, tempo_ciclo_ideal,
                        disponibilidade_percent, performance_percent, qualidade_percent, oee_percent
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    data_producao, horario_inicio, horario_fim, tempo_ciclo_ideal,
                    round(disponibilidade * 100, 2),
                    round(performance * 100, 2),
                    round(qualidade * 100, 2),
                    round(oee * 100, 2)
                ))

                print(f"✅ OEE atualizado às {datetime.now().strftime('%H:%M:%S')} — Total: {round(oee * 100, 2)}%")

    except Exception as e:
        print(f"❌ Erro ao calcular ou inserir o OEE: {e}")

def agendar_oee_diario():
    parametros = coletar_parametros()

    def job():
        agora = datetime.now()
        limite = datetime.combine(parametros["data_producao"], time_obj(23, 59, 59))
        if agora > limite:
            print("⏹️ Produção encerrada para o dia. OEE não será mais calculado.")
            return schedule.CancelJob
        calcular_oee_com_parametros(parametros)

    schedule.every(1).minutes.do(job)
    job()  # Executa uma vez imediatamente

    def loop_schedule():
        while True:
            schedule.run_pending()
            time.sleep(60)

    threading.Thread(target=loop_schedule, daemon=True).start()

if __name__ == "__main__":
    agendar_oee_diario()
    while True:
        time.sleep(60)
