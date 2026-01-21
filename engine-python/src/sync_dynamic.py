from .api_client import get_api_data
from .config import SEASON

def sync_injuries(cursor):
    print("Syncing Injuries (1 API call)...")
    data = get_api_data(f"/injuries?season={SEASON}&league=1")
    
    for record in data.get("response", []):
        p_id = record['player']['id']
        cursor.execute("""
            INSERT INTO injuries (player_id, injury_status, injury_reason, last_updated)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (player_id) DO UPDATE SET 
                injury_status = EXCLUDED.injury_status,
                injury_reason = EXCLUDED.injury_reason,
                last_updated = CURRENT_TIMESTAMP
        """, (p_id, record['player']['status'], record['player']['reason']))