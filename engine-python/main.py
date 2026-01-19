import psycopg2
import time
import os
import requests

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

def sync_from_sleeper():
    conn = connect_to_db()
    cur = conn.cursor()
    
    print("Python Engine: Syncing with Sleeper API...")
    try:
        response = requests.get("https://api.sleeper.app/v1/players/nfl")
        if response.status_code == 200:
            all_players = response.json()
            
            # We only want to sync specific offensive positions
            valid_positions = ['QB', 'RB', 'WR', 'TE']
            
            for p_id, info in all_players.items():
                if info.get('active') and info.get('position') in valid_positions:
                    name = info.get('full_name')
                    pos = info.get('position')
                    team = info.get('team') or 'FA' # Default to Free Agent if None
                    
                    # Update everything except points (keep points as is)
                    cur.execute("""
                        INSERT INTO players (name, position, team, points) 
                        VALUES (%s, %s, %s, 0)
                        ON CONFLICT (name) DO UPDATE SET 
                            position = EXCLUDED.position,
                            team = EXCLUDED.team;
                    """, (name, pos, team))
            
            conn.commit()
            print("Python Engine: Sync Complete!")
        else:
            print(f"Sleeper API Error: {response.status_code}")
    except Exception as e:
        print(f"Sync failed: {e}")
    finally:
        cur.close()
        conn.close()

# 1. Run sync once when container starts to populate the list
sync_from_sleeper()

# 2. Keep the container alive (optional: re-sync every 24 hours)
while True:
    time.sleep(3600)