import json
from src.api_client import get_tank01_data

def debug_odds_structure():
    print("--- Probing API for Raw Odds Data ---")
    # Date search is the most robust
    response = get_tank01_data("getNFLBettingOdds", {"gameDate": "20260125"})
    body = response.get('body', {})

    if not body:
        print("API returned an empty body. Check your subscription tier.")
        return

    for game_id, content in body.items():
        if game_id in ["last_updated_e_time", "gameDate"]: continue
        
        print(f"\n[GameID: {game_id}]")
        # List all top-level keys for this game (e.g., FanDuel, DraftKings)
        available_books = [k for k in content.keys() if isinstance(content[k], dict)]
        
        if not available_books:
            print(" -> Status: Matchup active, but NO sportsbooks have live lines.")
        else:
            print(f" -> Found lines from: {', '.join(available_books)}")
            # Show the first book's data as a sample
            sample_book = available_books[0]
            print(f" -> Sample data from {sample_book}:")
            print(json.dumps(content[sample_book], indent=2))

if __name__ == "__main__":
    debug_odds_structure()