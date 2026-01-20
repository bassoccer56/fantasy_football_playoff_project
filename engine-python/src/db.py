import psycopg2
import os
import time

def connect_to_db():
    """Handles the connection loop to the PostgreSQL database."""
    while True:
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "db"),
                database=os.getenv("DB_NAME", "fantasy_league"),
                user=os.getenv("DB_USER", "fantasy_admin"),
                password=os.getenv("DB_PASSWORD", "Sdf18943!@!")
            )
            return conn
        except Exception as e:
            print(f"Waiting for DB... {e}", flush=True)
            time.sleep(2)

def setup_table():
    """Applies the unique constraint to the players table."""
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("ALTER TABLE players ADD CONSTRAINT unique_player_name UNIQUE (name);")
        conn.commit()
        print("Database: Unique constraint verified.", flush=True)
    except Exception as e:
        conn.rollback()
        # We don't print the error if it's just 'already exists' to keep logs clean
        if "already exists" not in str(e):
            print(f"Database setup notice: {e}", flush=True)
    finally:
        cur.close()
        conn.close()