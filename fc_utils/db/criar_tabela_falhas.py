import psycopg2
from config import DB_CONFIG

def criar_tabela_falhas():
    comando_sql = """
    CREATE TABLE IF NOT EXISTS falhas (
        id SERIAL PRIMARY KEY,
        inicio_falha TIMESTAMP NOT NULL,
        fim_falha TIMESTAMP NOT NULL
    );
    """
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(comando_sql)
                print("✅ Tabela 'falhas' verificada/criada com sucesso.")
    except Exception as e:
        print("❌ Erro ao criar a tabela falhas:", e)
