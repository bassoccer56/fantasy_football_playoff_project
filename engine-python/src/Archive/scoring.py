import random
from .db import connect_to_db

def update_live_scores():
    """Simulates live game action by adding small point increments to active players."""
    conn = connect_to_db()
    cur = conn.cursor()
    
    try:
        # 1. Fetch all players currently in our DB
        cur.execute("SELECT name, position, points FROM players")
        players = cur.fetchall()
        
        print(f"Scoring Engine: Simulating action for {len(players)} players...", flush=True)

        for name, pos, current_points in players:
            # 2. Determine point 'boost' based on position probability
            # We use small floats to simulate yardage (0.1 points = 1 yard)
            increment = 0
            
            chance = random.random() # Random number between 0 and 1
            
            if pos == 'QB' and chance > 0.7: # 30% chance to gain yards
                increment = random.choice([0.04, 0.1, 0.4]) # Pass yard, or a 10yd gain
            elif pos in ['RB', 'WR', 'TE'] and chance > 0.85: # 15% chance for a play
                increment = random.choice([0.1, 0.5, 1.0, 6.0]) # Yardage or a Touchdown!

            if increment > 0:
                new_total = float(current_points) + increment
                cur.execute(
                    "UPDATE players SET points = %s WHERE name = %s",
                    (round(new_total, 2), name)
                )

        conn.commit()
        print("Scoring Engine: Live scores updated!", flush=True)

    except Exception as e:
        print(f"Scoring Error: {e}", flush=True)
        conn.rollback()
    finally:
        cur.close()
        conn.close()