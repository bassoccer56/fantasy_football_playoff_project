from src.api_client import get_tank01_data
import time

def get_full_offensive_adp():
    # List of all teams to check for data
    teams = [
        'SEA', 'LAR', 'NE', 'DEN', 'KC', 'BUF', 'PHI', 'SF', 
        'DAL', 'DET', 'BAL', 'HOU', 'GB', 'TB', 'CLE', 'MIA'
    ]
    
    all_offensive_players = []
    valid_pos = ['QB', 'RB', 'WR', 'TE']

    print("--- Scanning Team Rosters for ADP Data ---")

    for team in teams:
        print(f"Checking {team}...", end="\r")
        # Use getStats=true as Tank01 often bundles ADP with fantasy stats
        params = {"teamAbv": team, "getStats": "true"}
        response = get_tank01_data("getNFLTeamRoster", params)
        
        # Tank01 roster structure: body -> roster (list of players)
        roster = response.get('body', {}).get('roster', [])

        for player in roster:
            pos = player.get('pos')
            adp = player.get('fantasyADP')
            
            if pos in valid_pos and adp:
                all_offensive_players.append({
                    'name': player.get('longName'),
                    'team': team,
                    'pos': pos,
                    'adp': float(adp)
                })
        
        time.sleep(0.2) # Avoid hitting rate limits

    if not all_offensive_players:
        print("\n Status: No ADP data found in active rosters.")
        print("Note: ADP is often 'Reset' in late January to prepare for 2026 Rookie Drafts.")
        return

    # Sort by ADP (Ascending)
    all_offensive_players.sort(key=lambda x: x['adp'])

    print(f"\n{'Rank':<5} | {'Player Name':<25} | {'Pos':<4} | {'Team':<5} | {'ADP'}")
    print("-" * 60)

    for i, p in enumerate(all_offensive_players[:50], 1):
        print(f"{i:<5} | {p['name']:<25} | {p['pos']:<4} | {p['team']:<5} | {p['adp']:.1f}")

if __name__ == "__main__":
    get_full_offensive_adp()