import requests
import psycopg2
from psycopg2 import extras

# Configuration
API_KEY = "d0080b15e99cb3378f7c2e299fdec3a2"
DB_CONFIG = {"dbname": "fantasy_league", "user": "fantasy_admin", "password": "Sdf18943!@!", "host": "localhost"}

def sync_all_2023_games():
    url = "https://v1.american-football.api-sports.io/games"
    headers = {'x-apisports-key': API_KEY}
    params = {"league": "1", "season": "2023"}

    print("Fetching all 2023 NFL games...")
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    all_matches = data.get("response", [])

    game_records = []

    for item in all_matches:
        g = item.get('game', {})
        t = item.get('teams', {})
        s = item.get('scores', {})
        
        # FIXED: Extracting the string date from the date object
        date_info = g.get('date', {})
        clean_date = date_info.get('date') if isinstance(date_info, dict) else str(date_info)
        
        # Team and Score data
        home_id = t.get('home', {}).get('id')
        away_id = t.get('away', {}).get('id')
        home_score = s.get('home', {}).get('total')
        away_score = s.get('away', {}).get('total')
        
        # Status string
        status_str = g.get('status', {}).get('short', 'NS')

        record = (
            g.get('id'),
            clean_date,
            g.get('week'),
            home_id,
            away_id,
            home_score if home_score is not None else 0,
            away_score if away_score is not None else 0,
            status_str
        )

        # Safety check: Only add if we have a valid Game ID and Home ID
        if record[0] and record[3]:
            game_records.append(record)

    if not game_records:
        print("No games found.")
        return

    # Database Insertion
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        upsert_query = """
        INSERT INTO games (game_id, date, week, home_team_id, away_team_id, home_score, away_score, status)
        VALUES %s
        ON CONFLICT (game_id) DO UPDATE SET
            home_score = EXCLUDED.home_score,
            away_score = EXCLUDED.away_score,
            status = EXCLUDED.status;
        """

        extras.execute_values(cur, upsert_query, game_records)
        conn.commit()
        print(f"Successfully imported {len(game_records)} games (Full 2023 Season).")

    except Exception as e:
        print(f"Database Error: {e}")
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    sync_all_2023_games()