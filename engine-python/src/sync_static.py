import time
from .api_client import get_api_data
from .config import SEASON

def sync_teams(cursor):
    print("Syncing Teams...")
    data = get_api_data(f"/teams?league=1&season={SEASON}")
    for t in data.get("response", []):
        # Postgres Upsert Syntax
        cursor.execute("""
            INSERT INTO teams (team_id, team_name) VALUES (%s, %s)
            ON CONFLICT (team_id) DO UPDATE SET team_name = EXCLUDED.team_name
        """, (t['id'], t['name']))

def sync_players(cursor):
    print("Syncing Player Rosters...")
    cursor.execute("SELECT team_id FROM teams")
    teams = cursor.fetchall()
    
    for (t_id,) in teams:
        data = get_api_data(f"/players?team={t_id}&season={SEASON}")
        for p in data.get("response", []):
            if p['position'] in ['QB', 'RB', 'WR', 'TE']:
                name_parts = p['name'].split(' ', 1)
                f_name = name_parts[0]
                l_name = name_parts[1] if len(name_parts) > 1 else ""
                
                cursor.execute("""
                    INSERT INTO players (player_id, player_first_name, player_last_name, position, team_id) 
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (player_id) DO UPDATE SET 
                        player_first_name = EXCLUDED.player_first_name,
                        player_last_name = EXCLUDED.player_last_name,
                        position = EXCLUDED.position,
                        team_id = EXCLUDED.team_id
                """, (p['id'], f_name, l_name, p['position'], t_id))
        time.sleep(0.6)