const express = require('express');
const { Pool } = require('pg');
const path = require('path');

const app = express();

// Use process.env to pull variables from Docker/the .env file
const pool = new Pool({
  host: process.env.DB_HOST || 'db',
  database: process.env.POSTGRES_DB || 'fantasy_league',
  user: process.env.POSTGRES_USER || 'fantasy_admin',
  password: process.env.POSTGRES_PASSWORD, // This was the missing link!
  port: 5432,
});

// Middleware to serve your HTML frontend
app.use(express.static(path.join(__dirname, 'public')));

// API endpoint to fetch injury data
app.get('/api/injuries', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT p.player_name, t.team_abv, i.description, i.status 
      FROM injuries i 
      JOIN players p ON i.player_id = p.player_id
      JOIN teams t ON p.team_id = t.team_id
      ORDER BY t.team_abv ASC
    `);
    res.json(result.rows);
  } catch (err) {
    console.error('Database query error:', err.stack);
    res.status(500).json({ error: err.message });
  }
});

// Health check endpoint (helpful for debugging)
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', database: 'connected' });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Backend listening on port ${PORT}`);
  console.log(`Connecting to database at host: ${process.env.DB_HOST || 'db'}`);
});