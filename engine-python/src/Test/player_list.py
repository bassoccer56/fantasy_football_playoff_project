import http.client
import json
import time

API_KEY = "d0080b15e99cb3378f7c2e299fdec3a2"
conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")
headers = {'x-apisports-key': API_KEY}

def get_data(endpoint):
    conn.request("GET", endpoint, headers=headers)
    return json.loads(conn.getresponse().read().decode("utf-8"))

try:
    # STEP 1: Get all teams for the 2023 NFL season
    print("Fetching team list...")
    teams_data = get_data("/teams?league=1&season=2023")
    teams = teams_data.get("response", [])
    
    print(f"Found {len(teams)} teams. Starting player sync...\n")
    print(f"{'PLAYER ID':<10} | {'NAME':<25} | {'TEAM ID':<8} | {'TEAM NAME'}")
    print("-" * 75)

    # STEP 2: Loop through each team to get their roster
    for t_entry in teams:
        t_id = t_entry['id']
        t_name = t_entry['name']
        
        # Fetch players for this specific team
        player_path = f"/players?team={t_id}&season=2023"
        players_data = get_data(player_path)
        
        for p in players_data.get("response", []):
            print(f"{p['id']:<10} | {p['name']:<25} | {t_id:<8} | {t_name}")
        
        # Respect API rate limits (Small pause between team requests)
        time.sleep(0.5) 

except Exception as e:
    print(f"Error: {e}")