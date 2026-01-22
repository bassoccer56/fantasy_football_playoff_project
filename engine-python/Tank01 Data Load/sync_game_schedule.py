import psycopg2
from src.api_client import get_tank01_data
from src.config import DB_CONFIG

def sync_playoff_scores():
    conn = None
    try:
        print("Connecting to local PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Targeting 'post' season specifically for all playoff rounds
        print("Fetching Post-Season games and scores...")
        params = {
            "week": "all",
            "seasonType": "post",
            "season": "2025"  # The 2025 season playoffs happen in Jan 2026
        }
        
        data = get_tank01_data("getNFLGamesForWeek", params)
        games = data.get('body', [])

        if not games:
            print(" No post-season games found. Double-check your API access/season year.")
            return

        updated_count = 0
        for g in games:
            game_id = g.get('gameID')
            # Extract scores - Tank01 provides these in the schedule body for completed games
            away_score = int(g.get('awayScore', 0)) if g.get('awayScore') else 0
            home_score = int(g.get('homeScore', 0)) if g.get('homeScore') else 0
            status = g.get('gameStatus', 'Scheduled')

            cursor.execute("""
                INSERT INTO games (game_id, game_date, game_time, away_team, home_team, away_score, home_score, game_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (game_id) DO UPDATE SET 
                    away_score = EXCLUDED.away_score,
                    home_score = EXCLUDED.home_score,
                    game_status = EXCLUDED.game_status;
            """, (game_id, g.get('gameDate'), g.get('gameTime'), g.get('away'), g.get('home'), 
                  away_score, home_score, status))
            
            if status == "Final":
                print(f"   Final: {g['away']} {away_score} @ {g['home']} {home_score}")
                updated_count += 1
            else:
                print(f"   {status}: {g['away']} @ {g['home']}")

        conn.commit()
        print(f"\n SUCCESS: Synced {len(games)} playoff games ({updated_count} Final scores).")

    except Exception as e:
        print(f" ERROR: {e}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    sync_playoff_scores()