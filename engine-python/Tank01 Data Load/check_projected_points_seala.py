import json
from src.api_client import get_tank01_data

def check_seahawks_rams_projections():
    # Week 3 Postseason = Conference Championships
    params = {
        "week": "3",
        "seasonType": "post",
        "season": "2025"
    }

    target_game = "20260125_LAR@SEA"

    print(f"--- Fetching Projections for: {target_game} ---")
    response = get_tank01_data("getNFLProjections", params)
    projections = response.get('body', {})

    if not isinstance(projections, dict) or not projections:
        print("Status: API returned no data. Lines may be frozen due to injuries.")
        return

    # Filter for only players in the Rams @ Seahawks game
    game_players = [
        info for p_id, info in projections.items()
        if isinstance(info, dict) and info.get('gameID') == target_game
    ]

    if not game_players:
        print(f"Status: Matchup {target_game} found in schedule, but no player projections are live yet.")
        return

    # Sort by projected points (highest first)
    game_players.sort(key=lambda x: float(x.get('fantasyPointsDefault', 0)), reverse=True)

    print(f"{'Player Name':<25} | {'Team':<5} | {'Proj Pts':<10}")
    print("-" * 50)

    for p in game_players:
        name = p.get('longName', 'N/A')
        team = p.get('team', 'N/A')
        pts = p.get('fantasyPointsDefault', '0.0')
        
        print(f"{name:<25} | {team:<5} | {pts:<10}")

if __name__ == "__main__":
    check_seahawks_rams_projections()