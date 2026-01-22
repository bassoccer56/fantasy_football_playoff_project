import psycopg2
from src.api_client import get_tank01_data
from src.config import DB_CONFIG

def sync_all_box_scores():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 1. Get all game IDs from your database that likely have stats
        # We look for postseason games (Jan 2026)
        cursor.execute("SELECT game_id FROM games WHERE game_id LIKE '2026%'")
        game_ids = [row[0] for row in cursor.fetchall()]

        if not game_ids:
            print("No games found in the database to sync stats for.")
            return

        for g_id in game_ids:
            print(f"Syncing stats for game: {g_id}")
            data = get_tank01_data("getNFLBoxScore", {"gameID": g_id})
            
            # The stats are nested under 'body' -> 'playerStats'
            body = data.get('body', {})
            player_stats_map = body.get('playerStats', {})

            if not player_stats_map:
                print(f"  No player stats found in API for {g_id}")
                continue

            print(f"  Found {len(player_stats_map)} players with stats. Writing to DB...")

            for p_id, s in player_stats_map.items():
                # Helper function to safely convert to int/float
                def val(x, default=0):
                    if x is None or x == "": return default
                    try: return int(float(x))
                    except: return default

                cursor.execute("""
                    INSERT INTO player_game_stats (
                        game_id, player_id, pass_yds, pass_td, rush_yds, rush_td, 
                        receptions, rec_yds, rec_td, fumbles_lost, interceptions, fantasy_points
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (game_id, player_id) DO UPDATE SET 
                        pass_yds = EXCLUDED.pass_yds,
                        pass_td = EXCLUDED.pass_td,
                        rush_yds = EXCLUDED.rush_yds,
                        rush_td = EXCLUDED.rush_td,
                        receptions = EXCLUDED.receptions,
                        rec_yds = EXCLUDED.rec_yds,
                        rec_td = EXCLUDED.rec_td,
                        fantasy_points = EXCLUDED.fantasy_points
                """, (
                    g_id, p_id,
                    val(s.get('passYds')), val(s.get('passTD')),
                    val(s.get('rushYds')), val(s.get('rushTD')),
                    val(s.get('receptions')), val(s.get('recYds')),
                    val(s.get('recTD')), val(s.get('fumblesLost')),
                    val(s.get('int')), float(s.get('fantasyPointsDefault', 0.0))
                ))

        conn.commit()
        print("Final sync complete.")

    except Exception as e:
        print(f"Error during sync: {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    sync_all_box_scores()