import psycopg2
from config import DB_CONFIG

def criar_tabela_ciclo():
    comando_sql = """
    CREATE TABLE IF NOT EXISTS ciclo_pecas (
        id SERIAL PRIMARY KEY,
        inicio_ciclo TIMESTAMP NOT NULL,
        fim_ciclo TIMESTAMP NOT NULL,
        tempo_ciclo INTERVAL GENERATED ALWAYS AS (fim_ciclo - inicio_ciclo) STORED,
        qualidade INT NOT NULL
    );
    """
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(comando_sql)
                print("✅ Tabela 'ciclo_pecas' verificada/criada com sucesso.")
    except Exception as e:
        print("❌ Erro ao criar a tabela ciclo_pecas:", e)