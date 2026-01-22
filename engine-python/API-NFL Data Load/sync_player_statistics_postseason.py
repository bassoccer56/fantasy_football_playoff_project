import requests
import psycopg2
import time

# Configuration
API_KEY = "d0080b15e99cb3378f7c2e299fdec3a2"
DB_CONFIG = {
    "dbname": "fantasy_league", 
    "user": "fantasy_admin", 
    "password": "Sdf18943!@!", 
    "host": "localhost"
}

# Your specified game IDs
GAME_IDS = [7849, 10940, 13145, 7850, 13144, 7851, 10941, 7852, 10942, 7853, 10943, 7802, 7803]

def clean_val(val):
    """Safely converts API values like '16/21' or '0-0' to integers."""
    if val is None: return 0
    if isinstance(val, str):
        if '/' in val: val = val.split('/')[0]
        elif '-' in val: val = val.split('-')[0]
    try:
        return int(float(val))
    except:
        return 0

def sync_offensive_stats():
    url = "https://v1.american-football.api-sports.io/games/statistics/players"
    headers = {"x-apisports-key": API_KEY}
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Step 1: Ensure columns exist in the database
        cur.execute("""
            ALTER TABLE player_stats 
            ADD COLUMN IF NOT EXISTS receptions INTEGER DEFAULT 0,
            ADD COLUMN IF NOT EXISTS targets INTEGER DEFAULT 0,
            ADD COLUMN IF NOT EXISTS receiving_yards INTEGER DEFAULT 0,
            ADD COLUMN IF NOT EXISTS receiving_tds INTEGER DEFAULT 0,
            ADD COLUMN IF NOT EXISTS fumbles_lost INTEGER DEFAULT 0;
        """)
        conn.commit()

        for g_id in GAME_IDS:
            print(f"Processing Game ID: {g_id}...")
            response = requests.get(url, headers=headers, params={"id": g_id})
            
            if response.status_code != 200:
                print(f"Failed to fetch game {g_id}: {response.status_code}")
                continue
                
            data = response.json()

            for team_entry in data.get('response', []):
                t_id = team_entry['team']['id']
                
                for group in team_entry.get('groups', []):
                    group_name = group['name']
                    # Only process offensive groups
                    if group_name not in ['Passing', 'Rushing', 'Receiving']:
                        continue

                    for p_entry in group.get('players', []):
                        p_id = p_entry['player']['id']
                        # Map internal statistics to a temp dict
                        raw = {s['name']: s['value'] for s in p_entry['statistics']}

                        # Logic adjustments for specific offensive categories
                        p_yds = clean_val(raw.get('yards')) if group_name == 'Passing' else 0
                        p_tds = clean_val(raw.get('passing touch downs')) if group_name == 'Passing' else 0
                        r_yds = clean_val(raw.get('yards')) if group_name == 'Rushing' else 0
                        r_tds = clean_val(raw.get('rushing touch downs')) if group_name == 'Rushing' else 0
                        
                        # Fix: Changed 'receptions' to 'total receptions' and added 'targets'
                        rec = clean_val(raw.get('total receptions')) if group_name == 'Receiving' else 0
                        targ = clean_val(raw.get('targets')) if group_name == 'Receiving' else 0
                        rec_yds = clean_val(raw.get('yards')) if group_name == 'Receiving' else 0
                        rec_tds = clean_val(raw.get('receiving touch downs')) if group_name == 'Receiving' else 0
                        
                        fumb = clean_val(raw.get('fumbles lost'))
                        ints = clean_val(raw.get('interceptions')) if group_name == 'Passing' else 0

                        query = """
                            INSERT INTO player_stats (
                                game_id, player_id, team_id, passing_yards, passing_tds, 
                                interceptions, rushing_yards, rushing_tds, 
                                receptions, targets, receiving_yards, receiving_tds, fumbles_lost
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (game_id, player_id) DO UPDATE SET
                                passing_yards = player_stats.passing_yards + EXCLUDED.passing_yards,
                                passing_tds = player_stats.passing_tds + EXCLUDED.passing_tds,
                                interceptions = player_stats.interceptions + EXCLUDED.interceptions,
                                rushing_yards = player_stats.rushing_yards + EXCLUDED.rushing_yards,
                                rushing_tds = player_stats.rushing_tds + EXCLUDED.rushing_tds,
                                receptions = player_stats.receptions + EXCLUDED.receptions,
                                targets = player_stats.targets + EXCLUDED.targets,
                                receiving_yards = player_stats.receiving_yards + EXCLUDED.receiving_yards,
                                receiving_tds = player_stats.receiving_tds + EXCLUDED.receiving_tds,
                                fumbles_lost = player_stats.fumbles_lost + EXCLUDED.fumbles_lost;
                        """
                        cur.execute(query, (
                            g_id, p_id, t_id, p_yds, p_tds, ints, r_yds, r_tds, 
                            rec, targ, rec_yds, rec_tds, fumb
                        ))
            
            conn.commit()
            time.sleep(1) # Rate limit protection

        print("All games processed successfully.")

    except Exception as e:
        print(f"Critical Error: {e}")
    finally:
        if 'conn' in locals():
            cur.close()
            conn.close()

if __name__ == "__main__":
    sync_offensive_stats()