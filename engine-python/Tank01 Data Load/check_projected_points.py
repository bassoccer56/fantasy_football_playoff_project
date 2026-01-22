import time
from src.api_client import get_tank01_data

def check_projections_status():
    # Week 3 Postseason = Conference Championships
    params = {
        "week": "3",
        "seasonType": "post",
        "season": "2025"
    }

    print(f"[{time.strftime('%H:%M:%S')}] Checking Tank01 for Week 3 Projections...")
    response = get_tank01_data("getNFLProjections", params)
    projections = response.get('body', {})

    if isinstance(projections, dict) and len(projections) > 10:
        print(f" SUCCESS: Found {len(projections)} player projections.")
        
        # Spot check specific players affected by recent injuries
        print("\nSpot-Checking Key Players:")
        print(f"{'Player':<20} | {'Proj Pts':<10} | {'Team'}")
        print("-" * 45)
        
        for p_id, p_info in projections.items():
            name = p_info.get('longName', '')
            # Looking for the new starters/workhorses
            if "Stidham" in name or "Kenneth Walker" in name or "Purdy" in name:
                pts = p_info.get('fantasyPointsDefault', '0.0')
                team = p_info.get('team', 'N/A')
                print(f"{name:<20} | {pts:<10} | {team}")
    else:
        print(" STATUS: Projections are still pending.")
        print("Note: If matchups are set but pts are 0, Vegas props aren't live yet.")

if __name__ == "__main__":
    check_projections_status()