-- 1. Teams Table
CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY,
    team_name TEXT
);

-- 2. Players Table (Static Info)
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    player_first_name TEXT,
    player_last_name TEXT,
    position VARCHAR(5),
    team_id INTEGER REFERENCES teams(team_id)
);

-- 3. Injuries Table (Dynamic Info)
CREATE TABLE IF NOT EXISTS injuries (
    player_id INTEGER PRIMARY KEY REFERENCES players(player_id),
    injury_status TEXT,
    injury_reason TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);