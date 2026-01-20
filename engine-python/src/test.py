import http.client
import json

# Your API Key
API_KEY = "d0080b15e99cb3378f7c2e299fdec3a2"

conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")

headers = {
    'x-apisports-key': API_KEY
}

# Now using 'id' to represent the game ID
id = 7669 
team = 32
player = 2310

# We map our 'id' variable to the 'fixture' parameter required by the API
path = f"/games/statistics/players?id={id}&team={team}&player={player}"

# Make the request
conn.request("GET", path, headers=headers)

res = conn.getresponse()
data = res.read()

# Parse and print
parsed_data = json.loads(data.decode("utf-8"))
print(json.dumps(parsed_data, indent=4))