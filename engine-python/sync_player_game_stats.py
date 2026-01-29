import psycopg2
from src.api_client import get_tank01_data
from src.config import DB_CONFIG

def sync_game_stats(game_id):
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        querystring = {
            "gameID": game_id,
            "fantasyPoints": "true",
            "playByPlay": "true",
            "passYards": ".04", "passTD": "4", "passInterceptions": "-2",
            "pointsPerReception": "1", "rushYards": ".1", "rushTD": "6",
            "receivingYards": ".1", "receivingTD": "6",
            "twoPointConversions": "2",
            "fgMade": "3", "fgMissed": "-1", 
            "xpMade": "1", "xpMissed": "0",  
            "fumbles": "-2"
        }

        data = get_tank01_data("getNFLBoxScore", querystring)
        body = data.get('body', {})
        player_stats_map = body.get('playerStats', {})
        all_pbp = body.get('allPlayByPlay', [])

        if not player_stats_map:
            print(f"No stats found for game {game_id}.")
            return

        # --- STEP 1: FG DISTANCE MAPPING ---
        fg_distance_map = {}
        for play_info in all_pbp:
            play_text = play_info.get('play', '')
            if "field goal" in play_text.lower() and "is GOOD" in play_text:
                p_stats = play_info.get('playerStats', {})
                for pid, cats in p_stats.items():
                    kicking = cats.get('Kicking', {})
                    yards = kicking.get('fgYds')
                    if yards:
                        yards = int(float(yards))
                        if pid not in fg_distance_map:
                            fg_distance_map[pid] = {'30': 0, '40': 0, '50': 0, '60': 0}
                        
                        if yards < 40: fg_distance_map[pid]['30'] += 1
                        elif 40 <= yards < 50: fg_distance_map[pid]['40'] += 1
                        elif 50 <= yards < 60: fg_distance_map[pid]['50'] += 1
                        elif yards >= 60: fg_distance_map[pid]['60'] += 1

        # --- STEP 2: PROCESS & UPSERT ---
        for p_id, p_data in player_stats_map.items():
            
            def get_stat(category, key):
                val = p_data.get(category, {}).get(key, "0")
                try: return int(float(val))
                except (ValueError, TypeError): return 0

            # --- UPDATED FUMBLE LOGIC ---
            fumbles_lost = 0
            fumble_sources = ['fumbles', 'Rushing', 'Receiving', 'Passing', 'General', 'Defense']
            
            for source in fumble_sources:
                # Check for common key variations
                val = get_stat(source, 'fumblesLost')
                if val == 0:
                    val = get_stat(source, 'fumLost') # Shorthand check
                
                if val > 0:
                    fumbles_lost = val
                    print(f"DEBUG: Found {fumbles_lost} fumbles_lost in '{source}' for player {p_id}")
                    break 

            # Special Teams Logic
            p_ret_td = get_stat('Punting', 'puntReturnTD') or get_stat('Receiving', 'puntReturnTD')
            k_ret_td = get_stat('Kicking', 'kickReturnTD') or get_stat('Receiving', 'kickReturnTD')

            # Kicking Totals
            pat_made = get_stat('Kicking', 'xpMade') or get_stat('Kicking', 'patMade')
            pat_missed = get_stat('Kicking', 'xpMissed') or get_stat('Kicking', 'patMissed')
            fg_missed = get_stat('Kicking', 'fgMissed')
            dists = fg_distance_map.get(p_id, {'30': 0, '40': 0, '50': 0, '60': 0})

            # Offensive Stats
            pass_yds, pass_td, ints = get_stat('Passing', 'passYds'), get_stat('Passing', 'passTD'), get_stat('Passing', 'int')
            rush_yds, rush_td = get_stat('Rushing', 'rushYds'), get_stat('Rushing', 'rushTD')
            rec_yds, rec_td = get_stat('Receiving', 'recYds'), get_stat('Receiving', 'recTD')
            receptions, targets = get_stat('Receiving', 'receptions'), get_stat('Receiving', 'targets')
            
            two_pt = (get_stat('Passing', 'passingTwoPointConversion') + 
                      get_stat('Rushing', 'rushingTwoPointConversion') + 
                      get_stat('Receiving', 'receivingTwoPointConversion'))

            fg_made_total = sum(dists.values())
            
            # --- CUSTOM CALCULATION ---
            calc_pts = (
                (pass_yds * 0.04) + (pass_td * 4) - (ints * 2) +
                (rush_yds * 0.1) + (rush_td * 6) +
                (rec_yds * 0.1) + (rec_td * 6) +
                (receptions * 1) + (two_pt * 2) +
                (p_ret_td * 6) + (k_ret_td * 6) - (fumbles_lost * 2) +
                (pat_made * 1) + (pat_missed * 0) + (fg_missed * -1) +
                (dists['30'] * 3) + (dists['40'] * 4) + (dists['50'] * 5) + (dists['60'] * 6)
            )

            # Skip players with zero activity
            if calc_pts == 0 and float(p_data.get('fantasyPoints', 0)) == 0:
                continue

            cursor.execute("""
                INSERT INTO player_game_stats (
                    game_id, player_id, pass_yds, pass_td, interceptions, two_point_conversions,
                    rush_yds, rush_td, receptions, rec_targets, rec_yds, rec_td, fumbles_lost,
                    fg_made, fg_missed, pat_made, pat_missed, punt_ret_td, kick_ret_td,
                    fg_made_30yd, fg_made_40yd, fg_made_50yd, fg_made_60yd,
                    fantasy_points_calculated
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (game_id, player_id) DO UPDATE SET 
                    fumbles_lost = EXCLUDED.fumbles_lost,
                    two_point_conversions = EXCLUDED.two_point_conversions,
                    fg_made_30yd = EXCLUDED.fg_made_30yd,
                    fg_made_40yd = EXCLUDED.fg_made_40yd,
                    fg_made_50yd = EXCLUDED.fg_made_50yd,
                    fg_made_60yd = EXCLUDED.fg_made_60yd,
                    fantasy_points_calculated = EXCLUDED.fantasy_points_calculated;
            """, (
                game_id, p_id, pass_yds, pass_td, ints, two_pt,
                rush_yds, rush_td, receptions, targets, rec_yds, rec_td, fumbles_lost,
                fg_made_total, fg_missed, pat_made, pat_missed, p_ret_td, k_ret_td,
                dists['30'], dists['40'], dists['50'], dists['60'],
                calc_pts
            ))

        conn.commit()
        print(f"SUCCESS: Synced {game_id} with updated Fumble logic.")

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    sync_game_stats("20260118_HOU@NE")