CREATE TABLE IF NOT EXISTS teams (
    team_id VARCHAR(10) PRIMARY KEY,
    team_abv VARCHAR(10),
    team_city VARCHAR(50),
    team_name VARCHAR(50),
    conference VARCHAR(50),
    division VARCHAR(50),
    wins INTEGER DEFAULT 0,
    loss INTEGER DEFAULT 0,
    tie INTEGER DEFAULT 0,
    logo_url TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS players (
    player_id VARCHAR(50) PRIMARY KEY,
    team_id VARCHAR(10),  -- Changed from team_abv
    long_name VARCHAR(255),
    position VARCHAR(10),
    injury_designation VARCHAR(100),
    injury_desc TEXT,
    player_photo_url TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE games (
    game_id VARCHAR(50) PRIMARY KEY,
    game_date VARCHAR(20),
    game_time VARCHAR(20),
    away_team VARCHAR(10),
    home_team VARCHAR(10),
    away_score INTEGER DEFAULT 0,
    home_score INTEGER DEFAULT 0,
    game_status VARCHAR(50),
    game_quarter VARCHAR(10), -- e.g., "1", "2", "Half", "4"
    game_clock VARCHAR(10),   -- e.g., "12:45"
    last_updated TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE player_game_stats (
    game_id VARCHAR(50),
    player_id VARCHAR(50),
    pass_yds INT DEFAULT 0,
    pass_td INT DEFAULT 0,
    interceptions INT DEFAULT 0,
    two_point_conversions INT DEFAULT 0,
    rush_yds INT DEFAULT 0,
    rush_td INT DEFAULT 0,
    receptions INT DEFAULT 0,
    rec_targets INT DEFAULT 0,
    rec_yds INT DEFAULT 0,
    rec_td INT DEFAULT 0,
    fumbles_lost INT DEFAULT 0,
    fg_made INT DEFAULT 0,
    fg_missed INT DEFAULT 0,
    fg_made_30yd INT DEFAULT 0,
    fg_made_40yd INT DEFAULT 0,
    fg_made_50yd INT DEFAULT 0,
    fg_made_60yd INT DEFAULT 0,
    pat_made INT DEFAULT 0,
    pat_missed INT DEFAULT 0,
    punt_ret_td INT DEFAULT 0,
    kick_ret_td INT DEFAULT 0,
    fantasy_points_calculated NUMERIC(10, 2) DEFAULT 0.00,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Add this line
    PRIMARY KEY (game_id, player_id)
);