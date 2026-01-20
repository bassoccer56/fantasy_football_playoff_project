import requests
from collections import defaultdict

def get_fantasy_points(game_id):
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={game_id}"
    
    try:
        response = requests.get(url)
        data = response.json()
        teams = data.get('boxscore', {}).get('players', [])

        # This dictionary will store: { "Player Name": total_points }
        final_scores = defaultdict(float)

        for team_data in teams:
            team_name = team_data.get('team', {}).get('displayName')
            
            for category in team_data.get('statistics', []):
                cat_name = category.get('name')
                
                for athlete_data in category.get('athletes', []):
                    name = athlete_data.get('athlete', {}).get('displayName')
                    stats = athlete_data.get('stats', [])
                    points = 0.0
                    
                    # Logic based on your specific index results
                    if cat_name == 'passing' and len(stats) > 4:
                        yds, tds, ints = int(stats[1]), int(stats[3]), int(stats[4])
                        points = (yds * 0.04) + (tds * 4) - (ints * 2)
                        
                    elif cat_name == 'rushing' and len(stats) > 3:
                        yds, tds = int(stats[1]), int(stats[3])
                        points = (yds * 0.1) + (tds * 6)
                        
                    elif cat_name == 'receiving' and len(stats) > 3:
                        reps, yds, tds = int(stats[0]), int(stats[1]), int(stats[3])
                        points = (reps * 1.0) + (yds * 0.1) + (tds * 6)

                    elif cat_name == 'fumbles' and len(stats) > 1:
                        lost = int(stats[1])
                        points = (lost * -2.0)

                    # Add the points to the player's total in the dictionary
                    final_scores[name] += points

        # Print the final combined results
        print(f"\n--- Combined Fantasy Totals for Game {game_id} ---")
        # Sort by points (highest first)
        sorted_players = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        
        for name, total in sorted_players:
            if total != 0:
                print(f"{name.ljust(20)}: {round(total, 2)} total points")

    except Exception as e:
        print(f"Error calculating totals: {e}")

if __name__ == "__main__":
    get_fantasy_points("401772985")