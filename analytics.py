from sqlalchemy import text
from main import engine

def analyze_haaland_runs():
    # We use raw SQL to tap directly into PostGIS spatial functions
    query = text("""
        WITH PassMoments AS (
            -- Step 1: Find the exact timestamps when Foden releases the ball
            SELECT timestamp FROM events WHERE player_id = 'Foden_47' LIMIT 5
        ),
        HaalandPositions AS (
            -- Step 2: Get Haaland's (X,Y) location at those exact milliseconds
            SELECT timestamp, location AS haaland_loc 
            FROM events 
            WHERE player_id = 'Haaland_9' AND timestamp IN (SELECT timestamp FROM PassMoments)
        ),
        LastDefender AS (
            -- Step 3: Find the deepest Chelsea defender (lowest X coordinate) at that time
            SELECT e.timestamp, e.location AS def_loc
            FROM events e
            WHERE e.player_id LIKE 'Chelsea_%' 
            AND e.timestamp IN (SELECT timestamp FROM PassMoments)
            ORDER BY ST_X(e.location) ASC -- Lowest X means closest to their own goal
            LIMIT 5
        )
        
        -- Step 4: Calculate the spatial distance between Haaland and the Last Defender
        SELECT 
            h.timestamp, 
            ST_Distance(h.haaland_loc, d.def_loc) AS separation_distance
        FROM HaalandPositions h
        JOIN LastDefender d ON h.timestamp = d.timestamp;
    """)

    with engine.connect() as conn:
        result = conn.execute(query)
        print("\n🔍 HAALAND BLIND-SIDE RUN LOG (FED BY FODEN):")
        print("-" * 55)
        
        count = 0
        for row in result:
            count += 1
            print(f"⏱️ Time: {row.timestamp} | 📏 Separation: {round(row.separation_distance, 2)} meters")
            
        if count == 0:
            print("⚠️ No runs found! Did you run mock_data.py first?")
        print("-" * 55)

if __name__ == "__main__":
    analyze_haaland_runs()