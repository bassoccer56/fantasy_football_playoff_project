const express = require('express');
const { Pool } = require('pg');
const path = require('path');

const app = express();
const pool = new Pool({
    host: process.env.DB_HOST,
    database: process.env.DB_NAME,
    user: process.env.DB_USER,
    password: process.env.DB_PASS,
    port: 5432,
});

app.use(express.static('public'));

app.get('/api/stats', async (req, res) => {
    try {
        const query = `
            SELECT 
                SUBSTRING(s.game_id FROM '_(.*)') || ' ' || g.away_score || '-' || g.home_score AS game_info,
                p.player_photo_url,
                p.long_name,
                t.team_abv,
                p.position,
                g.game_quarter || ' ' || g.game_clock AS game_clock,
                s.fantasy_points_calculated,
                s.last_updated
            FROM player_game_stats s
            LEFT JOIN players p ON s.player_id = p.player_id
            LEFT JOIN teams t ON p.team_id = t.team_id
            LEFT JOIN games g ON s.game_id = g.game_id
            ORDER BY s.fantasy_points_calculated DESC;
        `;
        const result = await pool.query(query);
        res.json(result.rows);
    } catch (err) {
        console.error("Database Query Error:", err);
        res.status(500).send('Server Error');
    }
});

app.listen(3000, () => console.log('Web server running on http://localhost:3000'));