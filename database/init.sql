CREATE TABLE IF NOT EXISTS teams (
    team_id TEXT PRIMARY KEY,
    team_name TEXT,
    team_abv TEXT
);

CREATE TABLE IF NOT EXISTS players (
    player_id TEXT PRIMARY KEY,
    player_name TEXT,
    position TEXT,
    team_id TEXT REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS injuries (
    player_id TEXT PRIMARY KEY REFERENCES players(player_id),
    description TEXT,
    status TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);