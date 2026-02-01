from .api_client import get_tank01_data

def sync_playoff_scores(conn):
    """
    Syncs playoff game schedules and live scores.
    Accepts an active psycopg2 connection object.
    """
    cursor = None
    try:
        cursor = conn.cursor()

        # Step 1: Get the schedule to find all playoff game IDs
        print("Fetching Post-Season schedule...")
        schedule_params = {
            "week": "all",
            "seasonType": "post",
            "season": "2025" # Playoffs occurring in Jan/Feb 2026
        }
        
        schedule_data = get_tank01_data("getNFLGamesForWeek", schedule_params)
        games_list = schedule_data.get('body', [])

        if not games_list:
            print("   No playoff games found in the schedule.")
            return

        for game in games_list:
            game_id = game.get('gameID')
            print(f"   Syncing live data for: {game_id}...")

            # Step 2: Fetch the Live Box Score for this specific game
            box_data = get_tank01_data("getNFLBoxScore", {"gameID": game_id})
            body = box_data.get('body', {})
            line_score = body.get('lineScore', {})

            # Targeted extraction from the lineScore structure
            away_info = line_score.get('away', {})
            home_info = line_score.get('home', {})

            # Scores pulled from the nested 'totalPts'
            away_score = int(away_info.get('totalPts', 0))
            home_score = int(home_info.get('totalPts', 0))

            # Quarter/Period Logic: currentPeriod is primary, period is backup
            quarter = line_score.get('currentPeriod') or line_score.get('period') or 'Scheduled'
            clock = line_score.get('gameClock', '')
            status = body.get('gameStatus', game.get('gameStatus'))

            # Step 3: Upsert into PostgreSQL
            cursor.execute("""
                INSERT INTO games (
                    game_id, game_date, game_time, away_team, home_team, 
                    away_score, home_score, game_status, game_quarter, game_clock, last_updated
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (game_id) DO UPDATE SET 
                    away_score = EXCLUDED.away_score,
                    home_score = EXCLUDED.home_score,
                    game_status = EXCLUDED.game_status,
                    game_quarter = EXCLUDED.game_quarter,
                    game_clock = EXCLUDED.game_clock,
                    last_updated = CURRENT_TIMESTAMP;
            """, (
                game_id, game.get('gameDate'), game.get('gameTime'), game.get('away'), game.get('home'), 
                away_score, home_score, status, quarter, clock
            ))
            
            print(f"      [UPDATED] {game['away']} {away_score} @ {game['home']} {home_score} | {quarter} {clock}")

        conn.commit()
        print(f"\nSUCCESS: Synced {len(games_list)} games with live scores.")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"CRITICAL ERROR in sync_playoff_scores: {e}")
    finally:
        if cursor:
            cursor.close()