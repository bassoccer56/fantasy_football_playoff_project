import requests
import psycopg2
from psycopg2 import extras
import time

API_KEY = "d0080b15e99cb3378f7c2e299fdec3a2"
DB_CONFIG = {"dbname": "fantasy_league", "user": "fantasy_admin", "password": "Sdf18943!@!", "host": "localhost"}

def import_players():
    url = "https://v1.american-football.api-sports.io/players"
    headers = {'x-apisports-key': API_KEY}
    
    # We need to loop through team IDs 1 to 32
    for team_id in range(1, 33):
        print(f"Fetching players for Team ID: {team_id}...")
        params = {"team": team_id, "season": "2023"}
        
        response = requests.get(url, headers=headers, params=params)
        data = response.json().get("response", [])
        
        player_records = []
        for item in data:
            player_records.append((
                item['id'], item['name'], item['position'], 
                team_id, item.get('number'), item.get('image')
            ))

        if player_records:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            query = """INSERT INTO players (player_id, name, position, team_id, number, image_url) 
                       VALUES %s ON CONFLICT (player_id) DO NOTHING"""
            extras.execute_values(cur, query, player_records)
            conn.commit()
            cur.close()
            conn.close()
        
        time.sleep(1) # Respect rate limits (30 per minute usually)

if __name__ == "__main__":
    import_players()