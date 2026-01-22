import psycopg2
from src.api_client import get_tank01_data
from src.config import DB_CONFIG

def sync_game_stats(game_id):
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print(f"Fetching Box Score for {game_id}...")
        data = get_tank01_data("getNFLBoxScore", {"gameID": game_id})
        player_stats_map = data.get('body', {}).get('playerStats', {})

        if not player_stats_map:
            print(f"No stats found for game {game_id}.")
            return

        for p_id, p_data in player_stats_map.items():
            # Navigation Helper: Safely get nested values (e.g., p_data['Rushing']['rushYds'])
            def get_stat(category, key):
                return p_data.get(category, {}).get(key, "0")

            # Extracting stats based on your debug output structure
            pass_yds = int(get_stat('Passing', 'passYds'))
            pass_td  = int(get_stat('Passing', 'passTD'))
            rush_yds = int(get_stat('Rushing', 'rushYds'))
            rush_td  = int(get_stat('Rushing', 'rushTD'))
            rec_yds  = int(get_stat('Receiving', 'recYds'))
            rec_td   = int(get_stat('Receiving', 'recTD'))
            rec_count = int(get_stat('Receiving', 'receptions'))
            
            # Defense/Turnovers (adjusting keys based on typical Tank01 patterns)
            int_thrown = int(get_stat('Passing', 'int'))
            fumbles_lost = int(get_stat('Fumbles', 'fumblesLost'))

            # Manual Fantasy Point Calculation (Standard Scoring)
            # You can change these multipliers to match PPR or Half-PPR
            fantasy_pts = (
                (pass_yds * 0.04) + (pass_td * 4) - (int_thrown * 2) +
                (rush_yds * 0.1) + (rush_td * 6) +
                (rec_yds * 0.1) + (rec_td * 6) - (fumbles_lost * 2)
            )

            cursor.execute("""
                INSERT INTO player_game_stats (
                    game_id, player_id, pass_yds, pass_td, rush_yds, rush_td, 
                    receptions, rec_yds, rec_td, fumbles_lost, interceptions, fantasy_points
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (game_id, player_id) DO UPDATE SET 
                    pass_yds = EXCLUDED.pass_yds,
                    rush_yds = EXCLUDED.rush_yds,
                    rec_yds = EXCLUDED.rec_yds,
                    fantasy_points = EXCLUDED.fantasy_points;
            """, (
                game_id, p_id, pass_yds, pass_td, rush_yds, rush_td, 
                rec_count, rec_yds, rec_td, fumbles_lost, int_thrown, fantasy_pts
            ))

        conn.commit()
        print(f"SUCCESS: Synced {len(player_stats_map)} players for {game_id}.")

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    # Example for Wild Card game
    sync_game_stats("20260125_NE@DEN")