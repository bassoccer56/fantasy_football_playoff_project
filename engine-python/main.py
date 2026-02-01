import psycopg2
import time
from src.config import DB_CONFIG
from src.sync_teams import sync_teams

def main():
    sync_teams()

if __name__ == "__main__":
    main()