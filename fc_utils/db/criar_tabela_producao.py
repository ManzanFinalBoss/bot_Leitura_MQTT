import psycopg2
from config import DB_CONFIG

def criar_tabela_producao():
    comando_sql = """
    CREATE TABLE IF NOT EXISTS producao_pecas (
        id SERIAL PRIMARY KEY,
        inicio_prod TIMESTAMP NOT NULL,
        fim_prod TIMESTAMP NOT NULL,
        tempo_producao INTERVAL GENERATED ALWAYS AS (fim_prod - inicio_prod) STORED,
        qualidade INT NOT NULL
    );
    """
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(comando_sql)
                print("✅ Tabela 'producao_pecas' verificada/criada com sucesso.")
    except Exception as e:
        print("❌ Erro ao criar a tabela producao_pecas:", e)