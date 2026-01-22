import psycopg2
from src.api_client import get_tank01_data
from src.config import DB_CONFIG  # Uses the config we set up earlier

def sync_teams():
    conn = None
    try:
        # 1. Establish the connection to local Postgres
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 2. Fetch data from Tank01
        print("Fetching data from Tank01 NFL API...")
        data = get_tank01_data("getNFLTeams")
        
        # Check if we actually got data back
        teams = data.get('body', [])
        if not teams:
            print(" No data found in the API response. Check your API key!")
            return

        print(f"Successfully fetched {len(teams)} teams. Starting database sync...")

        # 3. Loop and Insert
        for t in teams:
            # We use t.get() to avoid KeyErrors if the API is missing a field
            team_id = t.get('teamID')
            team_abv = t.get('teamAbv')
            
            cursor.execute("""
                INSERT INTO teams (
                    team_id, team_abv, team_city, team_name, conference, 
                    division, wins, loss, tie, streak, logo_url
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (team_id) DO UPDATE SET 
                    wins = EXCLUDED.wins, 
                    loss = EXCLUDED.loss, 
                    streak = EXCLUDED.streak;
            """, (
                team_id, team_abv, t.get('teamCity'), t.get('teamName'),
                t.get('conference'), t.get('division'), 
                int(t.get('wins', 0)), int(t.get('loss', 0)), 
                int(t.get('tie', 0)), t.get('streak'), t.get('espnLogo1')
            ))
            
            # Print a small progress update for every team
            print(f"   Synced: {team_abv}")

        # 4. CRITICAL: Commit the changes
        conn.commit()
        print(f"\n SUCCESS: {len(teams)} teams saved to the database.")

    except Exception as e:
        print(f" DATABASE ERROR: {e}")
        if conn:
            conn.rollback()  # Undo changes if there's an error
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection closed.")

# --- THIS IS THE PART THAT ACTUALLY RUNS THE CODE ---
if __name__ == "__main__":
    sync_teams()