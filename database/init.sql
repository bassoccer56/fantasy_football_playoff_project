CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    position VARCHAR(10),
    team VARCHAR(10), -- Add this
    points INTEGER DEFAULT 0
);