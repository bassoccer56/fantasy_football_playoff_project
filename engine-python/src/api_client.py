import http.client
import json
from .config import API_SPORTS_KEY, BASE_URL

def get_api_data(endpoint):
    conn = http.client.HTTPSConnection(BASE_URL)
    headers = {'x-apisports-key': API_SPORTS_KEY}
    conn.request("GET", endpoint, headers=headers)
    return json.loads(conn.getresponse().read().decode("utf-8"))