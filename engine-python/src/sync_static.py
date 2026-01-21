import time
from .api_client import get_tank01_data

def sync_teams_and_players(cursor):
    print("Syncing Teams, Rosters, and Injuries...")
    
    # Tank01 returns a dictionary. The list of teams is in 'body'.
    full_response = get_tank01_data("getNFLTeams", {"rosters": "true"})
    
    # FIX: Get the list from the 'body' key. Default to empty list if not found.
    teams_list = full_response.get('body', [])
    
    print(f"DEBUG: API returned {len(teams_list)} teams.")

    for team in teams_list:
        t_id = team.get('teamID')
        if not t_id:
            continue
            
        # 1. Insert/Update Team
        cursor.execute("""
            INSERT INTO teams (team_id, team_name, team_abv) 
            VALUES (%s, %s, %s)
            ON CONFLICT (team_id) DO UPDATE SET 
                team_name = EXCLUDED.team_name,
                team_abv = EXCLUDED.team_abv
        """, (t_id, f"{team.get('teamCity')} {team.get('teamName')}", team.get('teamAbv')))

        # 2. Process Roster
        # Tank01 returns Roster as a dictionary where key is playerID
        roster = team.get('Roster', {})
        players_synced = 0
        
        for p_id, p in roster.items():
            pos = p.get('pos')
            if pos in ['QB', 'RB', 'WR', 'TE']:
                # Insert Player
                cursor.execute("""
                    INSERT INTO players (player_id, player_name, position, team_id)
                    VALUES (%s, %s, %s, %s) 
                    ON CONFLICT (player_id) DO UPDATE SET
                        player_name = EXCLUDED.player_name,
                        position = EXCLUDED.position,
                        team_id = EXCLUDED.team_id
                """, (p_id, p.get('longName'), pos, t_id))
                
                players_synced += 1
                
                # 3. Process Injury
                injury = p.get('injury')
                if injury:
                    # Handle cases where injury might be a string or a dict
                    desc = injury.get('description', 'No description') if isinstance(injury, dict) else str(injury)
                    status = p.get('espnStatus', 'Questionable')
                    
                    cursor.execute("""
                        INSERT INTO injuries (player_id, description, status)
                        VALUES (%s, %s, %s) 
                        ON CONFLICT (player_id) 
                        DO UPDATE SET description = EXCLUDED.description, status = EXCLUDED.status
                    """, (p_id, desc, status))
        
        print(f"  - Synced {team.get('teamAbv')}: {players_synced} fantasy players.")

    print("Sync complete!")