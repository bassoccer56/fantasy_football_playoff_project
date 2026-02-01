from .api_client import get_tank01_data

def sync_teams(conn):
    try:
        cursor = conn.cursor()
        print("Fetching data from Tank01 NFL API...")
        data = get_tank01_data("getNFLTeams")
        
        teams = data.get('body', [])
        if not teams:
            print(" No data found in the API response.")
            return

        for t in teams:
            cursor.execute("""
                INSERT INTO teams (
                    team_id, team_abv, team_city, team_name, conference, 
                    division, wins, loss, tie, logo_url
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (team_id) DO UPDATE SET 
                    wins = EXCLUDED.wins, 
                    loss = EXCLUDED.loss,
                    tie = EXCLUDED.tie,
                    last_updated = CURRENT_TIMESTAMP;
            """, (
                t.get('teamID'), t.get('teamAbv'), t.get('teamCity'), 
                t.get('teamName'), t.get('conference'), t.get('division'), 
                int(t.get('wins', 0)), int(t.get('loss', 0)), 
                int(t.get('tie', 0)), t.get('espnLogo1')
            ))
            
        conn.commit()
        print(f" SUCCESS: {len(teams)} teams saved.")
    except Exception as e:
        conn.rollback()
        print(f" DATABASE ERROR in teams: {e}")
    finally:
        cursor.close()