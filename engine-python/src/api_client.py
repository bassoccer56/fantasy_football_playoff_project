import requests
from .config import RAPID_API_KEY, API_HOST

def get_tank01_data(endpoint, params=None):
    url = f"https://{API_HOST}/{endpoint}"
    
    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": API_HOST
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        # This will now print the EXACT error message from RapidAPI
        if response.status_code != 200:
            print(f"API Error {response.status_code}: {response.text}")
            
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"DEBUG: Failed calling {endpoint}. Error: {e}")
        return {}