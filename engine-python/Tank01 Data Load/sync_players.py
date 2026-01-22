import psycopg2
from src.api_client import get_tank01_data
from src.config import DB_CONFIG

def sync_players():
    conn = None
    try:
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print("Fetching All Team Rosters (this may take a moment)...")
        data = get_tank01_data("getNFLTeams", {"rosters": "true"})
        teams = data.get('body', [])

        count = 0
        for team in teams:
            team_abv = team.get('teamAbv')
            roster = team.get('Roster', {})
            for p_id, p in roster.items():
                inj = p.get('injury', {})
                cursor.execute("""
                    INSERT INTO players (player_id, team_abv, long_name, position, status, injury_designation, injury_desc)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (player_id) DO UPDATE SET 
                        status=EXCLUDED.status, 
                        injury_designation=EXCLUDED.injury_designation,
                        injury_desc=EXCLUDED.injury_desc;
                """, (p_id, team_abv, p.get('longName'), p.get('pos'), p.get('espnStatus'), 
                      inj.get('designation'), inj.get('description')))
                count += 1
        
        conn.commit()
        print(f" SUCCESS: {count} players synced.")
    except Exception as e:
        print(f" ERROR: {e}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    sync_players()