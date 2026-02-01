import requests
import os

def get_tank01_data(endpoint, params=None):
    # Pull credentials from environment variables set in docker-compose.yml
    # This replaces the hardcoded imports from .config
    api_key = os.getenv("RAPIDAPI_KEY")
    api_host = os.getenv("API_HOST", "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com")
    
    if not api_key:
        print("ERROR: RAPIDAPI_KEY environment variable is missing!")
        return {}

    url = f"https://{api_host}/{endpoint}"
    
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": api_host
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        # Explicitly check for 403 (Subscription) or 429 (Rate Limit) errors
        if response.status_code != 200:
            print(f"API Error {response.status_code}: {response.text}")
            
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"DEBUG: Failed calling {endpoint}. Error: {e}")
        return {}