import psycopg2
from config import DB_CONFIG

def criar_tabela_produção():
    comando_sql = """
    CREATE TABLE IF NOT EXISTS produção (
        id SERIAL PRIMARY KEY,
        inicio_prod TIMESTAMP NOT NULL,
        fim_prod TIMESTAMP NOT NULL,
        tempo_prod INTERVAL GENERATED ALWAYS AS (fim_prod - inicio_prod) STORED
    );
    """
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(comando_sql)
                print("✅ Tabela 'produção' verificada/criada com sucesso.")
    except Exception as e:
        print("❌ Erro ao criar a tabela produção:", e)
