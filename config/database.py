# config/database.py
import os
import psycopg2
import psycopg2.extras
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL")
MONGO_URL    = os.getenv("MONGO_URL")

def get_connection():
    """
    Retourne une connexion PostgreSQL
    """
    return psycopg2.connect(POSTGRES_URL)

def get_mongo_db():
    """
    Retourne la base MongoDB lotto_db
    """
    client = MongoClient(MONGO_URL)
    return client["lotto_db"]

def test_connections():
    """
    Teste les deux connexions au démarrage
    """
    # Test PostgreSQL
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM tirages;")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        print(f"✅ PostgreSQL OK — {count} tirages en base")
    except Exception as e:
        print(f"❌ PostgreSQL ERREUR : {e}")

    # Test MongoDB
    try:
        db          = get_mongo_db()
        collections = db.list_collection_names()
        print(f"✅ MongoDB OK — collections : {collections}")
    except Exception as e:
        print(f"❌ MongoDB ERREUR : {e}")