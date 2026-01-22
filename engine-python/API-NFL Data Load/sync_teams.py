import requests
import psycopg2
from psycopg2 import extras

# Configuration
API_KEY = "d0080b15e99cb3378f7c2e299fdec3a2"
DB_CONFIG = {
    "dbname": "fantasy_league",
    "user": "fantasy_admin",
    "password": "Sdf18943!@!",
    "host": "localhost",
    "port": "5432"
}

def sync_nfl_data_from_standings():
    headers = {'x-apisports-key': API_KEY}
    url = "https://v1.american-football.api-sports.io/standings"
    
    # We use 2023 because it is a complete, stable dataset for your testing
    params = {"league": "1", "season": "2023"}

    print(f"Fetching 2023 NFL Standings...")
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Connection Error: {e}")
        return

    standings_data = data.get("response", [])
    if not standings_data:
        print("No data found in standings response.")
        return

    team_records = []
    for entry in standings_data:
        team = entry.get('team', {})
        t_id = team.get('id')
        
        if t_id:
            # Standings provides the ID, Name, Logo, Conf, and Div all in one object
            team_records.append((
                t_id,
                team.get('name'),
                team.get('code'), # Note: Standings might not have code, we'll handle it
                None,             # City (usually not in standings)
                entry.get('conference'),
                entry.get('division'),
                team.get('logo')
            ))

    if not team_records:
        print("Parsed 0 team records from standings.")
        return

    # Database Work
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # UPSERT: Insert or Update if team_id exists
        upsert_query = """
        INSERT INTO teams (team_id, name, code, city, conference, division, logo_url)
        VALUES %s
        ON CONFLICT (team_id) DO UPDATE SET
            name = EXCLUDED.name,
            conference = EXCLUDED.conference,
            division = EXCLUDED.division,
            logo_url = EXCLUDED.logo_url,
            last_updated = CURRENT_TIMESTAMP;
        """
        
        extras.execute_values(cur, upsert_query, team_records)
        conn.commit()
        print(f"Success: Imported/Updated {len(team_records)} teams from Standings.")
        
    except Exception as e:
        print(f"Database Error: {e}")
        if 'conn' in locals(): conn.rollback()
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    sync_nfl_data_from_standings()