import sqlite3
import http.client
import json
import time

# Configuration
API_SPORTS_KEY = "d0080b15e99cb3378f7c2e299fdec3a2"
DB_NAME = "fantasy_league.db"
SEASON = "2023"

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Clear existing tables (Drop child tables first)
    print("Refreshing database schema...")
    cursor.execute("DROP TABLE IF EXISTS injuries")
    cursor.execute("DROP TABLE IF EXISTS players")
    cursor.execute("DROP TABLE IF EXISTS teams")
    
    # 2. Teams Table
    cursor.execute('''CREATE TABLE teams (
                        team_id INTEGER PRIMARY KEY,
                        team_name TEXT)''')
    
    # 3. Players Table (Static Info)
    cursor.execute('''CREATE TABLE players (
                        player_id INTEGER PRIMARY KEY,
                        player_first_name TEXT,
                        player_last_name TEXT,
                        position TEXT,
                        team_id INTEGER,
                        FOREIGN KEY (team_id) REFERENCES teams(team_id))''')
    
    # 4. Injuries Table (Dynamic Info)
    # player_id is the Primary Key so each player has exactly one current status
    cursor.execute('''CREATE TABLE injuries (
                        player_id INTEGER PRIMARY KEY,
                        injury_status TEXT,
                        injury_reason TEXT,
                        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (player_id) REFERENCES players(player_id))''')
    
    conn.commit()
    return conn

def get_api_data(endpoint):
    conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")
    headers = {'x-apisports-key': API_SPORTS_KEY}
    conn.request("GET", endpoint, headers=headers)
    return json.loads(conn.getresponse().read().decode("utf-8"))

def sync_players_and_teams(db_conn):
    cursor = db_conn.cursor()
    
    # Sync Teams
    print("Syncing Teams...")
    teams_data = get_api_data(f"/teams?league=1&season={SEASON}")
    teams = teams_data.get("response", [])
    for t in teams:
        cursor.execute("INSERT OR REPLACE INTO teams (team_id, team_name) VALUES (?, ?)", 
                       (t['id'], t['name']))
    db_conn.commit()

    # Sync Players (Dimension data)
    print("Syncing Player Rosters...")
    for t in teams:
        t_id, t_name = t['id'], t['name']
        print(f"  -> Pulling {t_name}...")
        player_data = get_api_data(f"/players?team={t_id}&season={SEASON}")
        
        for p_record in player_data.get("response", []):
            if p_record['position'] in ['QB', 'RB', 'WR', 'TE']:
                name_parts = p_record['name'].split(' ', 1)
                f_name = name_parts[0]
                l_name = name_parts[1] if len(name_parts) > 1 else ""
                
                cursor.execute("""
                    INSERT OR REPLACE INTO players (player_id, player_first_name, player_last_name, position, team_id) 
                    VALUES (?, ?, ?, ?, ?)
                """, (p_record['id'], f_name, l_name, p_record['position'], t_id))
        
        time.sleep(0.6) # API Rate Limit protection
    db_conn.commit()

def sync_injuries(db_conn):
    """Separate function for high-frequency injury updates."""
    print("\nSyncing Injury Reports...")
    cursor = db_conn.cursor()
    
    # Using the dedicated injuries endpoint
    injury_data = get_api_data(f"/injuries?season={SEASON}&league=1")
    
    for record in injury_data.get("response", []):
        p_id = record['player']['id']
        status = record['player']['status']
        reason = record['player']['reason']
        
        cursor.execute("""
            INSERT OR REPLACE INTO injuries (player_id, injury_status, injury_reason, last_updated)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (p_id, status, reason))
    
    db_conn.commit()
    print("Injury sync finalized.")

def verify_normalized_data(db_conn):
    cursor = db_conn.cursor()
    
    print(f"\n{'='*40} MASTER ROSTER VIEW (JOINED) {'='*40}")
    # We use LEFT JOIN so we still see Healthy players who aren't in the injuries table
    query = """
        SELECT 
            p.player_id, 
            p.player_first_name, 
            p.player_last_name, 
            p.position, 
            t.team_name,
            COALESCE(i.injury_status, 'Healthy') as status,
            COALESCE(i.injury_reason, 'N/A') as reason
        FROM players p
        JOIN teams t ON p.team_id = t.team_id
        LEFT JOIN injuries i ON p.player_id = i.player_id
        LIMIT 50
    """
    
    header = f"{'ID':<6} | {'FIRST':<12} | {'LAST':<15} | {'POS':<4} | {'TEAM':<20} | {'STATUS':<12} | {'REASON'}"
    print(header)
    print("-" * len(header))
    
    cursor.execute(query)
    for row in cursor.fetchall():
        print(f"{row[0]:<6} | {row[1]:<12} | {row[2]:<15} | {row[3]:<4} | {row[4]:<20} | {row[5]:<12} | {row[6]}")

# Execution Flow
db = setup_database()
sync_players_and_teams(db)
sync_injuries(db)
verify_normalized_data(db)
db.close()