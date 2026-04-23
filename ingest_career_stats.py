import pandas as pd
from main import PlayerCareerStats, session, engine, Base

def ingest_haaland_career():
    print("📊 Ingesting Haaland Career Stats from player-groups.csv...")
    
    # Read semicolon-delimited CSV
    df = pd.read_csv("player-groups.csv", sep=";")
    
    # Ensure tables exist
    Base.metadata.create_all(engine)
    
    for _, row in df.iterrows():
        # Check for duplicates
        if not session.query(PlayerCareerStats).filter_by(
            player_name="Erling Haaland", 
            season=row['season']
        ).first():
            stat = PlayerCareerStats(
                player_name="Erling Haaland",
                season=row['season'],
                team=row['team'],
                apps=int(row['apps']),
                minutes=int(row['min']),
                goals=int(row['goals']),
                assists=int(row['assists']),
                xg=float(row['xG']),
                xa=float(row['xA']),
                xg90=float(row['xG90'])
            )
            session.add(stat)
    
    session.commit()
    print(f"✅ Successfully ingested {len(df)} seasons of Haaland data into PostGIS.")

if __name__ == "__main__":
    ingest_haaland_career()
