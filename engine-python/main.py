import time
import sys
from src.database import connect_to_db
from src.sync_static import sync_teams, sync_players
from src.sync_dynamic import sync_injuries
from src.test_db import test_select_all

def main():
    print(">>> Python Engine Starting...", flush=True)
    
    # Establish connection
    conn = connect_to_db()
    
    try:
        # 1. Check/Sync Initial Data
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM teams")
            if cur.fetchone()[0] == 0:
                print(">>> DB is empty. Running initial sync...", flush=True)
                sync_teams(cur)
                sync_players(cur)
                sync_injuries(cur)
                # CRITICAL: We must commit here so data is saved before the test runs
                conn.commit() 
            else:
                print(">>> Static data already exists. Skipping initial sync.", flush=True)
        
        # 2. Show Results (Pass the established conn)
        # We create a temporary cursor just for the test
        with conn.cursor() as test_cur:
            test_select_all(test_cur)

        # 3. Frequency Loop
        injury_timer = 0
        print(">>> Entering live monitoring loop...", flush=True)
        
        while True:
            with conn.cursor() as cur:
                if injury_timer >= 180:
                    print(">>> Syncing Injuries...", flush=True)
                    sync_injuries(cur)
                    conn.commit()
                    injury_timer = 0
            
            injury_timer += 1
            time.sleep(10)

    except Exception as e:
        print(f"!!! Engine Error: {e}", flush=True)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()