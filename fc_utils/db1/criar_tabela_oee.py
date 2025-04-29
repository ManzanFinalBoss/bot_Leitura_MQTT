import psycopg2
from config import DB_CONFIG

def criar_tabela_oee():
    comando_sql = """
    CREATE TABLE IF NOT EXISTS oee_diario (
        id SERIAL PRIMARY KEY,
        data_producao DATE NOT NULL,
        horario_inicio TIME NOT NULL,
        horario_fim TIME NOT NULL,
        tempo_ciclo_ideal DOUBLE PRECISION NOT NULL,
        disponibilidade_percent DOUBLE PRECISION,
        performance_percent DOUBLE PRECISION,
        qualidade_percent DOUBLE PRECISION,
        oee_percent DOUBLE PRECISION,
        data_insercao TIMESTAMP DEFAULT NOW()
    );
    """
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(comando_sql)
                print("✅ Tabela 'oee_diario' verificada/criada com sucesso.")
    except Exception as e:
        print("❌ Erro ao criar a tabela 'oee_diario':", e)

if __name__ == "__main__":
    criar_tabela_oee()
