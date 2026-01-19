import random
import time

players = ["Patrick Mahomes", "Justin Jefferson", "Christian McCaffrey"]

while True:
    # Create a fake stat
    player = random.choice(players)
    points = random.randint(0, 25)
    
    print(f"MOCK DATA: {player} just scored {points} points!")
    
    # NEXT STEP: Add code here to save this to your Postgres DB
    
    time.sleep(10) # Wait 10 seconds before the next "update"