import os
import psycopg2
from .config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

def connect_to_db():
    """Connects to the database using Docker environment variables."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", DB_HOST),
            database=os.getenv("DB_NAME", DB_NAME),
            user=os.getenv("DB_USER", DB_USER),
            password=os.getenv("DB_PASSWORD", DB_PASSWORD)
        )
        return conn
    except Exception as e:
        # Since Docker waits for health, a failure here is a real error
        print(f"Critical Error: Could not connect to database at {DB_HOST}. {e}")
        raise