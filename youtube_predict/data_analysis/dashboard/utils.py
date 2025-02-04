import sqlite3
import pandas as pd
import os

# Caminho correto do banco de dados
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Diretório do script utils.py
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "coleta_armazenamento", "youtube_data.db"))

# Função para carregar os dados do banco SQLite
def load_data():
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM videos"
    df = pd.read_sql(query, conn)
    conn.close()

    # Converter colunas para os tipos corretos
    df["published_at"] = pd.to_datetime(df["published_at"])

    # Evitar erro de divisão por zero ao calcular engajamento
    df["likes_per_view"] = df["likes"] / df["views"].replace(0, 1)

    return df
