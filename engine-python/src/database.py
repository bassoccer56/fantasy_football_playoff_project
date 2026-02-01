import psycopg2
import os
import time

def get_db_connection():
    """
    Connects to the PostgreSQL database.
    Uses environment variables for Docker and falls back to defaults for local development.
    """
    # Use environment variables passed from docker-compose, or fall back to defaults
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "fantasy_league_Tank01_Data")
    db_user = os.getenv("DB_USER", "fantasy_admin")
    db_pass = os.getenv("DB_PASS", "Sdf18943!@!")
    db_port = os.getenv("DB_PORT", "5432")

    while True:
        try:
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                database=db_name,
                user=db_user,
                password=db_pass
            )
            return conn
        except Exception as e:
            print(f"Database not ready yet at {db_host}... {e}")
            time.sleep(5)