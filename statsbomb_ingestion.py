import datetime
from statsbombpy import sb
from sqlalchemy.orm import sessionmaker
from main import MatchEvent, UnderstatShot, PlayerTrajectory, engine, session
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

# Match IDs
WC_FINAL_ID = 3869685
CITY_CHELSEA_ID = 3754066

def ingest_match_data(match_id, star_players, date_str):
    print(f"📡 Fetching StatsBomb Event Data for Match {match_id}...")
    events = sb.events(match_id=match_id)
    
    # 1. Ingest Shots
    shots = events[events.type == 'Shot']
    print(f"⚽ Found {len(shots)} shots. Ingesting...")
    for _, shot in shots.iterrows():
        if not session.query(UnderstatShot).filter_by(id=shot.id).first():
            x, y = shot.location
            new_shot = UnderstatShot(
                id=shot.id,
                minute=int(shot.minute),
                player=shot.player,
                team=shot.team,
                result=shot.shot_outcome,
                xg=float(shot.shot_statsbomb_xg),
                location=f"POINT({x} {y})"
            )
            session.add(new_shot)

    # 2. Ingest Trajectories
    for player_name in star_players:
        player_events = events[events.player == player_name].sort_values('timestamp')
        if player_events.empty: continue
        print(f"🏃 Processing {len(player_events)} events for {player_name}...")
        
        points = []
        timestamps = []
        for _, ev in player_events.iterrows():
            if isinstance(ev.location, list):
                points.append(f"{ev.location[0]} {ev.location[1]}")
                t_str = f"{date_str} {ev.timestamp}"
                timestamps.append(datetime.datetime.strptime(t_str, "%Y-%m-%d %H:%M:%S.%f"))
        
        if len(points) > 1:
            line_wkt = f"LINESTRING({', '.join(points)})"
            traj = PlayerTrajectory(
                player_id=player_name,
                start_time=timestamps[0],
                end_time=timestamps[-1],
                path=line_wkt
            )
            session.add(traj)
    session.commit()

if __name__ == "__main__":
    # Ingest WC Final
    ingest_match_data(WC_FINAL_ID, ['Lionel Andrés Messi Cuccittini', 'Kylian Mbappé Lottin'], "2022-12-18")
    
    # Ingest Man City vs Chelsea 2015/16
    ingest_match_data(CITY_CHELSEA_ID, ['Kevin De Bruyne', 'Sergio Leonel Agüero del Castillo'], "2015-08-16")
    
    print("✅ StatsBomb Ingestion Complete! World Cup and Man City data is now in PostGIS.")
