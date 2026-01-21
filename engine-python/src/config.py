import os

# API Settings
API_SPORTS_KEY = "d0080b15e99cb3378f7c2e299fdec3a2"
BASE_URL = "v1.american-football.api-sports.io"
SEASON = "2023"

# Database Credentials
DB_HOST = "db"
DB_NAME = "fantasy_league"
DB_USER = "fantasy_admin"
DB_PASSWORD = "Sdf18943!@!"


# Switch to read API key from dockerfile
#import os

# API Settings - Pull from Docker environment
# API_SPORTS_KEY = os.getenv("SPORTS_API_KEY", "your_fallback_key_here")
# SEASON = "2023"

# Database Credentials (defaults for local dev, overridden by Docker env)
# DB_HOST = os.getenv("DB_HOST", "localhost")
# DB_NAME = os.getenv("DB_NAME", "fantasy_league")
# DB_USER = os.getenv("DB_USER", "fantasy_admin")
# DB_PASSWORD = os.getenv("DB_PASSWORD", "Sdf18943!@!")