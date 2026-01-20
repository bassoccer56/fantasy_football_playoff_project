import requests

def get_active_nfl_games():
    """Fetches the current NFL scoreboard and prints game details and IDs."""
    # This is the public ESPN scoreboard endpoint
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        print("--- NFL SCOREBOARD ---")
        
        # 'events' contains all games for the current week
        for event in data.get('events', []):
            game_id = event.get('id')
            game_name = event.get('name') # e.g., "Chicago Bears at Green Bay Packers"
            
            # Status object contains the game state (Scheduled, In-Progress, or Final)
            status_info = event.get('status', {})
            status_name = status_info.get('type', {}).get('name')
            status_detail = status_info.get('type', {}).get('detail')
            
            # Print the game info to the console
            print(f"Game: {game_name}")
            print(f"ID: {game_id}")
            print(f"Status: {status_name} ({status_detail})")
            print("-" * 30)

    except Exception as e:
        print(f"Error fetching scoreboard: {e}")

if __name__ == "__main__":
    get_active_nfl_games()