import requests
from .db import connect_to_db

def sync_from_sleeper():
    """Fetches player data from Sleeper and upserts into the database."""
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
        print(f"Sync failed: {e}", flush=True)