import psycopg2
import time
from src.config import DB_CONFIG
from src.sync_static import sync_teams_and_players

def main():
    while True:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            sync_teams_and_players(cur)
            conn.commit()
            cur.close()
            conn.close()
            print("Sync successful. Sleeping for 1 hour...")
            time.sleep(3600)
        except Exception as e:
            print(f"Connection failed: {e}. Retrying in 10s...")
            time.sleep(10)

if __name__ == "__main__":
    main()