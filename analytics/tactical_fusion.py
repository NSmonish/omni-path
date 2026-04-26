import numpy as np
from analytics.temporal_tda import TacticalPersistenceTracker
from analytics.pitch_control import VectorizedPitchControl

class TacticalFusionEngine:
    """
    The 'Master Brain' of Omni-Path.
    Fuses Topological Data Analysis (TDA) with Physics-based Pitch Control.
    """
    def __init__(self):
        self.tda_tracker = TacticalPersistenceTracker(min_area_threshold=80, stability_frames=3)
        self.pitch_engine = VectorizedPitchControl()

    def analyze_frame(self, team_a_pos, team_a_vel, team_b_pos, team_b_vel):
        """
        1. Identifies stable passing lanes (Holes).
        2. Validates them against Pitch Control probability.
        """
        # Step 1: Get Stable Holes via TDA
        all_players = np.vstack([team_a_pos, team_b_pos])
        stable_hole_ids = self.tda_tracker.update(all_players)
        
        # Get coordinates of these holes
        holes = []
        for h_id in stable_hole_ids:
            hole_data = self.tda_tracker.active_holes[h_id]
            coord = hole_data['centroid']
            
            # Step 2: Check Pitch Control at this coordinate
            # We calculate who reaches the hole's centroid first
            time_a = min([self.pitch_engine.time_to_reach(coord, p, v) for p, v in zip(team_a_pos, team_a_vel)])
            time_b = min([self.pitch_engine.time_to_reach(coord, p, v) for p, v in zip(team_b_pos, team_b_vel)])
            
            # Probability that Team A (City) controls this hole
            control_prob = 1 / (1 + np.exp(time_a - min(time_a, time_b) - (time_b - min(time_a, time_b)))) # Simplified logistic
            control_prob = 1 / (1 + np.exp(time_a - time_b))

            holes.append({
                'id': h_id,
                'coord': coord,
                'control_score': round(control_prob, 3),
                'is_exploitable': control_prob > 0.6
            })
            
        return holes

if __name__ == "__main__":
    engine = TacticalFusionEngine()
    
    # Simulation: City Attacker sprinting into a gap between 2 Chelsea defenders
    city_pos = np.array([[60, 40], [55, 30]])
    city_vel = np.array([[9, 0], [5, 0]]) # Haaland is flying
    
    chelsea_pos = np.array([[75, 35], [75, 45], [85, 40]])
    chelsea_vel = np.array([[1, 0], [1, 0], [0, 0]]) # Defenders are slow to react
    
    print("🧠 Fusing Topology and Physics for Tactical Intelligence...")
    
    # Run for 4 frames to establish stability
    for i in range(4):
        opportunities = engine.analyze_frame(city_pos, city_vel, chelsea_pos, chelsea_vel)
    
    print(f"✅ Analysis Complete. Found {len(opportunities)} Validated Tactical Opportunities.")
    for opp in opportunities:
        status = "🔥 EXPLOITABLE" if opp['is_exploitable'] else "⚠️ TRAP"
        print(f"   - Hole {opp['id']} at {opp['coord']}: Control {opp['control_score']} | {status}")
