import psycopg2
import os
import time

def get_db_connection():
    # Use environment variables passed from docker-compose
    while True:
        try:
            conn = psycopg2.connect(
                host="db",
                database="fantasy_league",
                user="fantasy_admin",
                password=os.getenv("DB_PASSWORD")
            )
            return conn
        except Exception as e:
            print(f"Database not ready yet... {e}")
            time.sleep(5)