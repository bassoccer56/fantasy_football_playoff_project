import http.client
import json

# Your API Key
API_KEY = "d0080b15e99cb3378f7c2e299fdec3a2"

conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")
headers = {'x-apisports-key': API_KEY}

def calculate_group_points(group_name, stats_list):
    """Calculates points for a specific category with PPR logic."""
    pts = 0.0
    # Extract stat values into a helper dictionary for cleaner math
    s = {item['name'].lower(): (item['value'] if item['value'] is not None else 0) for item in stats_list}
    
    group_name = group_name.lower()
    
    if group_name == 'passing':
        # Passing: 1pt/25yds (0.04), 4pt/TD, -2pt/INT
        pts += (int(s.get('yards', 0)) * 0.04)
        pts += (int(s.get('touchdowns', 0)) * 4)
        pts += (int(s.get('interceptions', 0)) * -2)
        
    elif group_name == 'rushing':
        # Rushing: 1pt/10yds (0.1), 6pt/TD
        pts += (int(s.get('yards', 0)) * 0.1)
        pts += (int(s.get('rushing touch downs', 0)) * 6)
        
    elif group_name == 'receiving':
        # NEW: Receiving points using "total receptions"
        receptions = int(s.get('total receptions', 0))
        pts += (receptions * 1.0)  # 1 Point Per Reception (PPR)
        pts += (int(s.get('yards', 0)) * 0.1)
        pts += (int(s.get('receiving touch downs', 0)) * 6)
        
    return pts

# Fetching the full game
path = "/games/statistics/players?id=7669"

try:
    conn.request("GET", path, headers=headers)
    response = conn.getresponse()
    data = json.loads(response.read().decode("utf-8"))
    
    # Store aggregated scores to handle players in multiple groups
    master_scoreboard = {}

    for team_entry in data.get("response", []):
        t_name = team_entry['team']['name']
        
        for group in team_entry.get("groups", []):
            g_name = group['name']
            
            # Aggregate stats for Passing, Rushing, and Receiving
            if g_name in ['Passing', 'Rushing', 'Receiving']:
                for p_data in group.get("players", []):
                    p_name = p_data['player']['name']
                    points = calculate_group_points(g_name, p_data.get("statistics", []))
                    
                    if p_name not in master_scoreboard:
                        master_scoreboard[p_name] = {"team": t_name, "points": 0.0}
                    
                    master_scoreboard[p_name]["points"] += points

    # Display Leaderboard
    print(f"\n{'PPR FANTASY LEADERBOARD (ID 7669)':<30} | {'TEAM':<20} | {'POINTS'}")
    print("-" * 70)
    
    # Sort by points descending
    sorted_board = sorted(master_scoreboard.items(), key=lambda x: x[1]['points'], reverse=True)
    
    for name, info in sorted_board:
        if info['points'] > 0.1:
            print(f"{name:<30} | {info['team']:<20} | {info['points']:.2f}")

except Exception as e:
    print(f"Error: {e}")