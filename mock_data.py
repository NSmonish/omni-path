import datetime
from main import MatchEvent, PlayerTrajectory, session, engine
from sqlalchemy import func

def inject_5_runs():
    print("⏳ Injecting 5 specific Haaland runs with Trajectories...")
    
    # We create 5 exact timestamps (e.g., the 10th, 15th, 20th minutes of the match)
    base_time = datetime.datetime(2026, 4, 15, 20, 0, 0)
    timestamps = [base_time + datetime.timedelta(minutes=i*5) for i in range(5)]

    # 5 Scenarios: [Haaland (X,Y), Last Defender (X,Y)]
    scenarios = [
        ((18, 40), (20, 42)),   # Run 1: Haaland ghosting 2 meters past the line
        ((25, 50), (25.5, 48)), # Run 2: Haaland right on the shoulder
        ((10, 30), (15, 35)),   # Run 3: Deep penetrating run
        ((30, 60), (32, 55)),   # Run 4: Beating the high press
        ((5, 45), (8, 50))      # Run 5: Six-yard box tap-in
    ]

    player_paths = {"Haaland_9": [], "Foden_47": [], "Chelsea_CB": []}

    for i, t in enumerate(timestamps):
        h_pos, d_pos = scenarios[i]

        # 1. The Trigger
        foden = MatchEvent(player_id="Foden_47", timestamp=t, location='POINT(50 50)', velocity_mag=2.0, velocity_theta=180.0)
        player_paths["Foden_47"].append(f'POINT(50 50)')
        
        # 2. The Attacker
        haaland = MatchEvent(player_id="Haaland_9", timestamp=t, location=f'POINT({h_pos[0]} {h_pos[1]})', velocity_mag=8.8, velocity_theta=180.0)
        player_paths["Haaland_9"].append(f'POINT({h_pos[0]} {h_pos[1]})')
        
        # 3. The Target
        defender = MatchEvent(player_id="Chelsea_CB", timestamp=t, location=f'POINT({d_pos[0]} {d_pos[1]})', velocity_mag=3.0, velocity_theta=0.0)
        player_paths["Chelsea_CB"].append(f'POINT({d_pos[0]} {d_pos[1]})')

        session.add_all([foden, haaland, defender])

    # --- AGGREGATE INTO TRAJECTORIES ---
    for p_id, points in player_paths.items():
        # Create a LINESTRING from the list of points
        line_wkt = f"LINESTRING({', '.join([p.replace('POINT(', '').replace(')', '') for p in points])})"
        traj = PlayerTrajectory(
            player_id=p_id,
            start_time=timestamps[0],
            end_time=timestamps[-1],
            path=line_wkt
        )
        session.add(traj)

    session.commit()
    print("✅ Match events AND Trajectories successfully logged to PostGIS!")

if __name__ == "__main__":
    inject_5_runs()