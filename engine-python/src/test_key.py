import json
from api_client import get_tank01_data

def debug_stat_keys(game_id):
    print(f"--- Debugging Stat Keys for: {game_id} ---")
    response = get_tank01_data("getNFLBoxScore", {"gameID": game_id})
    body = response.get('body', {})
    player_stats = body.get('playerStats', {})

    if not player_stats:
        print("No player stats found.")
        return

    # Grab the first player's data to inspect the structure
    first_player_id = list(player_stats.keys())[0]
    first_player_data = player_stats[first_player_id]

    print(f"RAW DATA FOR PLAYER {first_player_id}:")
    print(json.dumps(first_player_data, indent=2))
    
    # Check if the stats are inside sub-categories
    print("\n--- Summary of Available Keys ---")
    for key, value in first_player_data.items():
        if isinstance(value, dict):
            print(f"Category [{key}] contains: {list(value.keys())}")
        else:
            print(f"Direct Key [{key}]: {value}")

if __name__ == "__main__":
    # Use your confirmed working Game ID
    debug_stat_keys("20260110_GB@CHI")