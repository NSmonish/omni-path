import soccerdata as sd
import pandas as pd

def fetch_haaland_data():
    print("📡 Connecting to FBref via SoccerData...")
    
    # Initialize FBref scraper for Premier League 2024-2025
    # Note: SoccerData handles the scraping and caching automatically
    fbref = sd.FBref(leagues="ENG-Premier League", seasons="2425")
    
    print("📈 Fetching Match Logs for Erling Haaland...")
    try:
        # Get match logs for all players in the league
        # We'll filter for Haaland later
        logs = fbref.read_player_match_stats(stat_type="summary")
        
        # In SoccerData/FBref, Haaland is usually 'Erling Haaland'
        # We need to find his specific index in the multi-index DataFrame
        haaland_logs = logs[logs.index.get_level_values('player') == 'Erling Haaland']
        
        if not haaland_logs.empty:
            print(f"✅ Success! Found {len(haaland_logs)} match entries for Haaland.")
            print(haaland_logs[['goals', 'xg', 'shots']].head())
            haaland_logs.to_csv("haaland_match_logs.csv")
        else:
            print("⚠️ Haaland not found in the 24/25 summary logs. Trying 'shooting' stats...")
            shooting = fbref.read_player_match_stats(stat_type="shooting")
            haaland_shooting = shooting[shooting.index.get_level_values('player') == 'Erling Haaland']
            print(f"✅ Success! Found {len(haaland_shooting)} shooting entries.")
            haaland_shooting.to_csv("haaland_shooting_logs.csv")

    except Exception as e:
        print(f"❌ Error fetching data: {e}")

if __name__ == "__main__":
    fetch_haaland_data()
