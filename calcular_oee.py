import psycopg2
import schedule
import time
import threading
import os
from dotenv import load_dotenv
from datetime import datetime, time as time_obj, timedelta
from zoneinfo import ZoneInfo
from config import DB_CONFIG

# Carrega .env se existir (para testes locais)
load_dotenv()

def coletar_parametros():
    try:
        data_str = os.getenv("DATA_PRODUCAO")
        horario_inicio_str = os.getenv("HORARIO_INICIO")
        horario_fim_str = os.getenv("HORARIO_FIM")
        tempo_ciclo_ideal_str = os.getenv("TEMPO_CICLO")
        intervalo_minutos_str = os.getenv("INTERVALO_CALCULO")

        if not all([data_str, horario_inicio_str, horario_fim_str, tempo_ciclo_ideal_str]):
            raise ValueError("Alguma variável de ambiente obrigatória não foi definida!")

        return {
            "data_producao": datetime.strptime(data_str, "%Y-%m-%d").date(),
            "horario_inicio": datetime.strptime(horario_inicio_str, "%H:%M:%S").time(),
            "horario_fim": datetime.strptime(horario_fim_str, "%H:%M:%S").time(),
            "tempo_ciclo_ideal": float(tempo_ciclo_ideal_str),
            "intervalo_minutos": int(intervalo_minutos_str) if intervalo_minutos_str else 60
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
                # 🔧 Corrigido: puxar inicio_prod e ajustar fuso corretamente
                cur.execute("""
                    SELECT inicio_prod
                    FROM produção
                    WHERE fim_prod IS NULL AND DATE(inicio_prod) = %s
                    ORDER BY inicio_prod ASC
                    LIMIT 1;
                """, (data_producao,))
                row = cur.fetchone()

                if row and row[0]:
                    inicio_prod_utc = row[0].replace(tzinfo=ZoneInfo("UTC"))  # dado está como SP, mas sem timezone
                    inicio_prod_sp = inicio_prod_utc.astimezone(ZoneInfo("America/Sao_Paulo"))  # converte para SP real
                    agora = datetime.now(ZoneInfo("America/Sao_Paulo"))
                    tempo_andamento = (agora - inicio_prod_sp).total_seconds()
                else:
                    tempo_andamento = 0

                # Tempo finalizado (normal)
                cur.execute("""
                    SELECT SUM(EXTRACT(EPOCH FROM tempo_prod))
                    FROM produção
                    WHERE tempo_prod IS NOT NULL AND DATE(inicio_prod) = %s;
                """, (data_producao,))
                tempo_finalizado = float(cur.fetchone()[0] or 0)

                tempo_produzido = tempo_finalizado + tempo_andamento

                # Peças
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

                agora = datetime.now(ZoneInfo("America/Sao_Paulo")).time()
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

                pecas_teoricas = tempo_produzido / tempo_ciclo_ideal if tempo_ciclo_ideal > 0 else 0
                disponibilidade = tempo_produzido / tempo_programado_segundos if tempo_programado_segundos > 0 else 0
                performance = total_pecas / pecas_teoricas if pecas_teoricas > 0 else 0
                qualidade = pecas_boas / total_pecas if total_pecas > 0 else 0
                oee = disponibilidade * performance * qualidade

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

                print(f"✅ OEE atualizado às {datetime.now(ZoneInfo('America/Sao_Paulo')).strftime('%H:%M:%S')} — Total: {round(oee * 100, 2)}%")

    except Exception as e:
        print(f"❌ Erro ao calcular ou inserir o OEE: {e}")

def agendar_oee_diario():
    parametros = coletar_parametros()

    def job():
        agora = datetime.now(ZoneInfo("America/Sao_Paulo"))

        if agora.time() < parametros["horario_inicio"]:
            print("⏳ Aguardando horário de início da produção...")
            return

        limite = datetime.combine(parametros["data_producao"], time_obj(23, 59, 59))
        limite = limite.replace(tzinfo=ZoneInfo("America/Sao_Paulo"))

        if agora > limite:
            print("⏹️ Produção encerrada para o dia. OEE não será mais calculado.")
            return schedule.CancelJob

        calcular_oee_com_parametros(parametros)

    now = datetime.now(ZoneInfo("America/Sao_Paulo"))

    inicio_dt = datetime.combine(parametros["data_producao"], parametros["horario_inicio"])
    inicio_dt = inicio_dt.replace(tzinfo=ZoneInfo("America/Sao_Paulo")) + timedelta(minutes=10)

    delay_inicial = max((inicio_dt - now).total_seconds(), 0)

    def loop_schedule():
        time.sleep(delay_inicial)
        schedule.every(parametros["intervalo_minutos"]).minutes.do(job)
        job()
        while True:
            schedule.run_pending()
            time.sleep(60)

    threading.Thread(target=loop_schedule, daemon=True).start()

if __name__ == "__main__":
    agendar_oee_diario()
    while True:
        time.sleep(60)
