import time
from src.db import setup_table
from src.sleeper import sync_from_sleeper
from src.scoring import update_live_scores

if __name__ == "__main__":
    setup_table()
    
    # Sync initial data once
    sync_from_sleeper()
    
    # Counter to track when to re-sync with Sleeper (e.g., every 60 intervals)
    sync_timer = 0
    
    while True:
        # 1. Run the scoring simulation every 10 seconds
        update_live_scores()
        
        # 2. Check if it's time to re-sync rosters from Sleeper (every 10 mins)
        if sync_timer >= 60:
            sync_from_sleeper()
            sync_timer = 0
        
        sync_timer += 1
        time.sleep(10)