import psycopg2
import time
import os

def connect_to_db():
    # Keep trying until the database is ready
    while True:
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "db"),
                database=os.getenv("DB_NAME", "fantasy_league"),
                user=os.getenv("DB_USER", "fantasy_admin"),
                password=os.getenv("DB_PASSWORD", "Sdf18943!@!")
            )
            print("Python Engine: Successfully connected to the database!")
            return conn
        except Exception as e:
            print(f"Database not ready yet... waiting 2 seconds. (Error: {e})")
            time.sleep(2)

# This will now wait patiently for the DB
conn = connect_to_db()
cur = conn.cursor()

def update_mock_score():
    try:
        # We use 'name' for the conflict check since we haven't assigned IDs manually
        cur.execute("""
            INSERT INTO players (name, position, points) 
            VALUES ('Patrick Mahomes', 'QB', 25)
            ON CONFLICT (name) DO UPDATE SET points = players.points + 1;
        """)
        conn.commit()
        print("Python Engine: Updated player scores in DB.")
    except Exception as e:
        print(f"Update failed: {e}")
        conn.rollback()

while True:
    update_mock_score()
    time.sleep(10)