import os
from dotenv import load_dotenv

# Load variables from your .env file
load_dotenv()

# --- Tank01 NFL API Settings ---
# It's best to keep your key in the .env file and only use the default as a backup
RAPID_API_KEY = os.getenv("RAPID_API_KEY", "your_fallback_key_here")
API_HOST = "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"

# --- PostgreSQL Database Configuration ---
# 'localhost' is used because Postgres is now running directly on your Windows OS
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "fantasy_league"),
    "user": os.getenv("DB_USER", "fantasy_admin"),
    "password": os.getenv("DB_PASSWORD", "Sdf18943!@!"),
    "host": os.getenv("DB_HOST", "localhost"),  # Changed from 'db' to 'localhost'
    "port": os.getenv("DB_PORT", "5432")       # Default Postgres port for local
}