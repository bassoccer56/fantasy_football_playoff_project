from .api_client import get_tank01_data

def sync_all_skill_players(conn):
    try:
        cursor = conn.cursor()
        data = get_tank01_data("getNFLPlayerList", {})
        all_players = data.get('body', [])
        target_positions = {'QB', 'RB', 'WR', 'TE', 'PK'}
        count = 0

        for p in all_players:
            pos = p.get('pos')
            if pos in target_positions:
                cursor.execute("""
                    INSERT INTO players (
                        player_id, team_id, long_name, position, 
                        injury_designation, injury_desc, player_photo_url
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (player_id) DO UPDATE SET 
                        team_id = EXCLUDED.team_id,
                        last_updated = CURRENT_TIMESTAMP;
                """, (
                    p.get('playerID'), p.get('teamID'), p.get('longName'), pos, 
                    p.get('injury', {}).get('designation'), 
                    p.get('injury', {}).get('description'), 
                    p.get('espnHeadshot')
                ))
                count += 1

        conn.commit()
        print(f" SUCCESS: {count} players synced.")
    except Exception as e:
        conn.rollback()
        print(f" ERROR in players: {e}")
    finally:
        cursor.close()