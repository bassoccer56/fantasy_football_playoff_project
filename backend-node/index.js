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
// Serves images, CSS, and index.html automatically from the public folder
app.use(express.static(path.join(__dirname, 'public')));

// 3. ROUTES
// Explicit home route (fallback)
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// The API endpoint for player data
app.get('/players', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM players ORDER BY points DESC');
    res.json(result.rows);
  } catch (err) {
    console.error("DETAILED DATABASE ERROR:", err.message);
    res.status(500).send(`Database error: ${err.message}`);
  }
});

// 4. START SERVER
app.listen(port, '0.0.0.0', () => {
  console.log(`API listening at http://localhost:${port}`);
});