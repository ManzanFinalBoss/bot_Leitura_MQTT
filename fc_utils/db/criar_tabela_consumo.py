import psycopg2
from config import DB_CONFIG

def criar_tabela_consumo():
    comando_sql = """
    CREATE TABLE IF NOT EXISTS consumo (
        id SERIAL PRIMARY KEY,
        horario TIMESTAMP NOT NULL,
        consumo_ar FLOAT,
        consumo_energia FLOAT
    );
    """
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(comando_sql)
                print("✅ Tabela 'consumo' verificada/criada com sucesso.")
    except Exception as e:
        print("❌ Erro ao criar a tabela consumo:", e)
