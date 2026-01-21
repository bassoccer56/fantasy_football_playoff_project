const express = require('express');
const { Pool } = require('pg');
const path = require('path');

const app = express();
const port = 3000;

// 1. DATABASE CONFIGURATION
const pool = new Pool({
  host: process.env.DB_HOST || 'db',
  user: process.env.DB_USER || 'fantasy_admin',
  password: process.env.DB_PASSWORD || 'Sdf18943!@!',
  database: process.env.DB_NAME || 'fantasy_league',
  port: 5432,
});

// 2. MIDDLEWARE
app.use(express.static(path.join(__dirname, 'public')));

// 3. ROUTES
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Main Endpoint: Joins Players, Teams, and Injuries
app.get('/players', async (req, res) => {
  try {
    const query = `
      SELECT 
        p.player_id, 
        p.player_first_name || ' ' || p.player_last_name AS name, 
        p.position, 
        t.team_name AS team,
        COALESCE(i.injury_status, 'Healthy') AS status,
        COALESCE(i.injury_reason, 'N/A') AS reason
      FROM players p
      JOIN teams t ON p.team_id = t.team_id
      LEFT JOIN injuries i ON p.player_id = i.player_id
      ORDER BY t.team_name ASC, p.player_last_name ASC
    `;
    const result = await pool.query(query);
    res.json(result.rows);
  } catch (err) {
    console.error("DATABASE ERROR:", err.message);
    res.status(500).send(`Database error: ${err.message}`);
  }
});

// Optional: Endpoint for just teams
app.get('/teams', async (req, res) => {
    const result = await pool.query('SELECT * FROM teams ORDER BY team_name');
    res.json(result.rows);
});

// 4. START SERVER
app.listen(port, '0.0.0.0', () => {
  console.log(`API listening at http://localhost:${port}`);
});