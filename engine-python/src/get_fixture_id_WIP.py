import http.client
import json

API_KEY = "d0080b15e99cb3378f7c2e299fdec3a2"
conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")
headers = {'x-apisports-key': API_KEY}

# Query a specific week in the 2023 Regular Season
path = "/games?league=1&season=2023"

try:
    conn.request("GET", path, headers=headers)
    data = json.loads(conn.getresponse().read().decode("utf-8"))
    
    print(f"{'GAME ID':<8} | {'STATUS':<5} | {'MATCHUP'}")
    print("-" * 45)

    for g in data.get("response", []):
        game_id = g['game']['id']
        # The API-Sports structure for status
        status_short = g['game']['status']['short']
        home = g['teams']['home']['name']
        away = g['teams']['away']['name']
        
        print(f"{game_id:<8} | {status_short:<5} | {away} @ {home}")

except Exception as e:
    print(f"Error: {e}")