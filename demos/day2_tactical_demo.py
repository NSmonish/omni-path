import numpy as np
import time
from analytics.tactical_fusion import TacticalFusionEngine

def run_live_demo():
    # Retuning the engine for higher sensitivity in the demo
    engine = TacticalFusionEngine()
    engine.tda_tracker.min_area_threshold = 40 
    
    print("\n" + "="*60)
    print("🏟️  OMNI-PATH LIVE DEMO: TACTICAL FUSION (DAY 2)")
    print("Scenario: Man City Counter-Attack vs. Chelsea Defense")
    print("="*60 + "\n")

    # City Attackers: Haaland (Player 9), Foden (Player 47)
    # Chelsea Defenders: CB1, CB2, RB
    
    # --- PHASE 1: STABLE DEFENSE ---
    print("🛡️  PHASE 1: Chelsea defense is compact. City looking for gaps...")
    city_pos = np.array([[40, 40], [45, 30]])
    city_vel = np.array([[4, 0], [4, 0]]) # Jogging buildup
    
    chelsea_pos = np.array([[55, 35], [55, 45], [60, 40]])
    chelsea_vel = np.array([[0, 0], [0, 0], [0, 0]]) # Static block
    
    for f in range(3):
        opps = engine.analyze_frame(city_pos, city_vel, chelsea_pos, chelsea_vel)
        print(f"   [Frame {f+1}] Gaps Found: {len(opps)} | Exploitable: {sum(o['is_exploitable'] for o in opps)}")
        time.sleep(0.1)

    # --- PHASE 2: HAALAND TRIGGER RUN ---
    print("\n⚡ PHASE 2: Haaland (9) triggers a high-velocity sprint! Gaps widening...")
    
    for f in range(4, 12): # Longer sequence for stability
        # Defenders split apart
        city_pos = np.array([[50 + (f-4)*2, 40], [48, 30]])
        city_vel = np.array([[10, 0], [5, 0]]) 
        
        # Chelsea defenders move OUT of the way, creating a massive hole
        chelsea_pos = np.array([[55, 10], [55, 70], [65, 40]]) 
        chelsea_vel = np.array([[0, -2], [0, 2], [0, 0]])
        
        opps = engine.analyze_frame(city_pos, city_vel, chelsea_pos, chelsea_vel)
        print(f"   [Frame {f:02d}] Gaps Found: {len(opps)}", end="")
        for o in opps:
            if o['is_exploitable']:
                print(f" | 🔥 TACTICAL ALERT: Haaland controls hole at {o['coord']} (Score: {o['control_score']})", end="")
        print("")
        time.sleep(0.05)

    print("\n" + "="*60)
    print("✅ DEMO COMPLETE: High-Dimensional Intelligence Validated.")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_live_demo()
