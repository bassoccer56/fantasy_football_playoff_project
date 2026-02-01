import psycopg2
from .api_client import get_tank01_data
from .config import DB_CONFIG

def sync_all_skill_players():
    conn = None
    try:
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print("Fetching full NFL Player List (includes IR and Inactive)...")
        # getNFLPlayerList returns all players in the Tank01 database
        data = get_tank01_data("getNFLPlayerList", {})
        all_players = data.get('body', [])

        # Define the positions we care about
        target_positions = {'QB', 'RB', 'WR', 'TE','PK'}
        count = 0

        for p in all_players:
            pos = p.get('pos')
            
            # Filter for specific positions
            if pos in target_positions:
                p_id = p.get('playerID')
                team_id = p.get('teamID')
                long_name = p.get('longName')
                
                # Injury data is nested in the 'injury' object
                injury_obj = p.get('injury', {})
                injury_designation = injury_obj.get('designation')
                injury_desc = injury_obj.get('description')
                
                # Fetch the headshot URL
                player_photo_url = p.get('espnHeadshot')

                cursor.execute("""
                    INSERT INTO players (
                        player_id, team_id, long_name, position, 
                        injury_designation, injury_desc, player_photo_url
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (player_id) DO UPDATE SET 
                        team_id = EXCLUDED.team_id,
                        long_name = EXCLUDED.long_name,
                        position = EXCLUDED.position,
                        injury_designation = EXCLUDED.injury_designation,
                        injury_desc = EXCLUDED.injury_desc,
                        player_photo_url = EXCLUDED.player_photo_url,
                        last_updated = CURRENT_TIMESTAMP;
                """, (
                    p_id, team_id, long_name, pos, 
                    injury_designation, injury_desc, player_photo_url
                ))
                count += 1

        conn.commit()
        print(f" SUCCESS: {count} skill-position players (including IR) synced.")

    except Exception as e:
        print(f" ERROR: {e}")
    finally:
        if conn:
            conn.close()