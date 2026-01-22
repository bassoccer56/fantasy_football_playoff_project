

CREATE TABLE teams (
    team_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(10),
    city VARCHAR(100),
    conference VARCHAR(50),
    division VARCHAR(50),
    logo_url TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE players (
    player_id INT PRIMARY KEY,
    name VARCHAR(150),
    position VARCHAR(10),
    team_id INT,
    number INT,
    image_url TEXT
);

CREATE TABLE games (
    game_id INT PRIMARY KEY,
    date TIMESTAMP,
    week VARCHAR(100),
    home_team_id INT,
    away_team_id INT,
    home_score INT,
    away_score INT,
    status VARCHAR(50),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Player Stats: The box score for fantasy calculations
CREATE TABLE player_stats (
    stat_id SERIAL PRIMARY KEY,
    game_id INT,
    player_id INT,
    team_id INT,
    passing_yards INT DEFAULT 0,
    passing_tds INT DEFAULT 0,
    interceptions INT DEFAULT 0,
    rushing_yards INT DEFAULT 0,
    rushing_tds INT DEFAULT 0,
    receptions INT DEFAULT 0,
    receiving_yards INT DEFAULT 0,
    receiving_tds INT DEFAULT 0,
    fumbles_lost INT DEFAULT 0
);