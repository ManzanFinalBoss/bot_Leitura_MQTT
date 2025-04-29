from dotenv import load_dotenv
import os

load_dotenv()

# Configurações do banco de dados PostgreSQL
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

# Configurações do Broker MQTT
MQTT_CONFIG = {
    "broker": os.getenv("MQTT_BROKER"),
    "port": int(os.getenv("MQTT_PORT")),
    "topics": [
        os.getenv("MQTT_TOPICO_1"),
        os.getenv("MQTT_TOPICO_2")
    ]
}
