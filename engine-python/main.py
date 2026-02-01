import os
import sys
import time
from src.database import get_db_connection
from src.sync_teams import sync_teams
from src.sync_players import sync_all_skill_players
from src.sync_game_schedule import sync_playoff_scores
from src.sync_player_game_stats import sync_game_stats

def main():
    # Establish connection once to be shared across all sync functions
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database. Exiting.")
        sys.exit(1)

    try:
        print("--- Starting Sync Sequence ---")
        
        # 1. Sync Teams
        sync_teams(conn)
        print("Waiting 5 seconds to respect API rate limits...")
        time.sleep(5) 

        # 2. Sync Players
        sync_all_skill_players(conn)
        print("Waiting 5 seconds to respect API rate limits...")
        time.sleep(5)

        # 3. Sync Game Schedule (Playoffs)
        sync_playoff_scores(conn)
        print("Waiting 5 seconds to respect API rate limits...")
        time.sleep(5)
        
        # 4. Sync Specific Game Stats
        # Note: If your sync_playoff_scores fetches many games, 
        # you may need more delays inside that function's loop.
        sync_game_stats(conn, "20251218_LAR@SEA")
        
        print("--- Sync Complete ---")
        
    except Exception as e:
        print(f"Critical Error during sync: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()