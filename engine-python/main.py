import time
from src.db import setup_table
from src.sleeper import sync_from_sleeper

if __name__ == "__main__":
    # Ensure database constraints are set
    setup_table()
    
    # Run the first sync immediately
    sync_from_sleeper()
    
    # Keep the service alive and sync periodically
    while True:
        # For example, sync once every hour (3600 seconds)
        # or stick to your 60-second loop for live testing
        time.sleep(3600)
        sync_from_sleeper()