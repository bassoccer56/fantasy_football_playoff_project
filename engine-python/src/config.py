import os

# API Settings
API_SPORTS_KEY = "d0080b15e99cb3378f7c2e299fdec3a2"
RAPID_API_KEY="dfda76b64dmshc04842ad36742b9p199581jsndcfb1b5bd1b2"
BASE_URL = "v1.american-football.api-sports.io"

# Database Credentials
DB_HOST = "db"
DB_NAME = "fantasy_league"
DB_USER = "fantasy_admin"
POSTGRES_PASSWORD = "Sdf18943!@!"


import os

API_KEY = os.getenv("RAPID_API_KEY","dfda76b64dmshc04842ad36742b9p199581jsndcfb1b5bd1b2")
API_HOST = "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
DB_CONFIG = {
    "dbname": "fantasy_league",
    "user": "fantasy_admin",
    "password": "Sdf18943!@!",
    "host": "db"
}