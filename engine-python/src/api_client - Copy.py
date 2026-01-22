import requests
import os

def get_tank01_data(endpoint, params=None):
    api_key = os.getenv("RAPID_API_KEY")
    url = f"https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com/{endpoint}"
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
    }

    try:
        print(f"DEBUG: Calling API {endpoint}...")
        response = requests.get(url, headers=headers, params=params)
        
        # Check for HTTP errors (like 403 Forbidden or 401 Unauthorized)
        response.raise_for_status() 
        
        return response.json()
    except Exception as e:
        print(f"API Error fetching {endpoint}: {e}")
        return {} # Return empty dict so the loop doesn't crash but skips