import psycopg2
import time
import os
import random

def connect_to_db():
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
            print(f"Waiting for DB... {e}")
            time.sleep(2)

conn = connect_to_db()
cur = conn.cursor()

# Our "Stub" Data
mock_players = [
    {"name": "Patrick Mahomes", "pos": "QB"},
    {"name": "Lamar Jackson", "pos": "QB"},
    {"name": "Christian McCaffrey", "pos": "RB"},
    {"name": "Tyreek Hill", "pos": "WR"}
]

while True:
    for p in mock_players:
        # Generate a random score bump between 0 and 5
        score_gain = random.randint(0, 5)
        
        cur.execute("""
            INSERT INTO players (name, position, points) 
            VALUES (%s, %s, %s)
            ON CONFLICT (name) DO UPDATE SET points = players.points + %s;
        """, (p['name'], p['pos'], score_gain, score_gain))
    
    conn.commit()
    print("Python Engine: Scores updated!")
    time.sleep(5) # Update every 5 seconds for testing