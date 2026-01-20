import psycopg2
import time
import os
import requests
import sys

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
            print(f"Waiting for DB... {e}", flush=True)
            time.sleep(2)

def setup_table():
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("ALTER TABLE players ADD CONSTRAINT unique_player_name UNIQUE (name);")
        conn.commit()
        print("Database: Unique constraint verified.", flush=True)
    except Exception as e:
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def sync_from_sleeper():
    print("Python Engine: Fetching data from Sleeper...", flush=True)
    try:
        response = requests.get("https://api.sleeper.app/v1/players/nfl")
        if response.status_code == 200:
            all_players = response.json()
            conn = connect_to_db()
            cur = conn.cursor()
            
            valid_positions = ['QB', 'RB', 'WR', 'TE']
            count = 0
            
            for p_id, info in all_players.items():
                if info.get('active') and info.get('position') in valid_positions:
                    name = info.get('full_name')
                    pos = info.get('position')
                    team = info.get('team') or 'FA'
                    
                    if name:
                        cur.execute("""
                            INSERT INTO players (name, position, team, points) 
                            VALUES (%s, %s, %s, 0)
                            ON CONFLICT (name) DO UPDATE SET 
                                position = EXCLUDED.position,
                                team = EXCLUDED.team;
                        """, (name, pos, team))
                        count += 1
            
            conn.commit()
            cur.close()
            conn.close()
            print(f"Python Engine: Sync Complete! {count} players added.", flush=True)
        else:
            print(f"Sleeper API Error: {response.status_code}", flush=True)
    except Exception as e:
        # FIXED: Corrected the missing parenthesis below
        print(f"Sync failed: {e}", flush=True)

if __name__ == "__main__":
    setup_table()
    sync_from_sleeper()
    while True:
        time.sleep(60)
