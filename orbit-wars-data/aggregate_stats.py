import json
from collections import defaultdict

def aggregate():
    with open("docs/episodes/summary.json") as f:
        summary = json.load(f)
        
    wins = []
    losses = []
    self_plays = []
    
    for r in summary:
        filename = r["filename"]
        rewards = r["rewards"]
        is_self_play = r["is_self_play"]
        
        if is_self_play:
            self_plays.append(r)
        else:
            our_idx = r["our_indices"][0]
            our_reward = rewards[our_idx]
            opp_idx = 1 - our_idx
            opp_reward = rewards[opp_idx] if len(rewards) > opp_idx else -1
            
            if our_reward > opp_reward:
                wins.append(r)
            else:
                losses.append(r)
                
    print(f"Wins: {len(wins)} | Losses: {len(losses)} | Self-Plays: {len(self_plays)}")
    
    def get_avg(group, key_dict_name):
        total_fleets = 0
        total_ships = 0
        total_oob = 0
        total_sun = 0
        total_planet = 0
        total_steps = 0
        
        count = len(group)
        if count == 0:
            return {}
            
        for r in group:
            our_idx = r["our_indices"][0] if r["our_indices"] else 0
            total_steps += r["steps"]
            total_fleets += r["fleets_launched"].get(str(our_idx), 0)
            total_ships += r["ships_launched"].get(str(our_idx), 0)
            total_oob += r["oob_fleets"].get(str(our_idx), 0)
            total_sun += r["sun_collisions"].get(str(our_idx), 0)
            total_planet += r["planet_collisions"].get(str(our_idx), 0)
            
        return {
            "avg_steps": total_steps / count,
            "avg_fleets": total_fleets / count,
            "avg_ships": total_ships / count,
            "avg_size": (total_ships / total_fleets) if total_fleets > 0 else 0,
            "oob_rate": (total_oob / total_fleets * 100) if total_fleets > 0 else 0,
            "sun_rate": (total_sun / total_fleets * 100) if total_fleets > 0 else 0,
            "planet_rate": (total_planet / total_fleets * 100) if total_fleets > 0 else 0,
        }

    print("\n--- AGGREGATED STATS FOR OUR AGENT ---")
    print("Wins Group:", get_avg(wins, "our"))
    print("Losses Group:", get_avg(losses, "our"))
    print("Self-Play Group:", get_avg(self_plays, "our"))

aggregate()
