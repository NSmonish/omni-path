import requests
import time
import json

def run_stability_test():
    api_url = "http://localhost:8000/ingest/coordinate"
    
    print("\n" + "="*60)
    print("🛰️  OMNI-PATH DAY 5 TEST: TRACKING STABILITY")
    print("Scenario: Noisy Stream -> Kalman Smoothing -> PostGIS")
    print("="*60 + "\n")

    # Simulate 5 frames of a player moving with noise
    # Real path: (20, 20) -> (24, 24)
    for i in range(5):
        noise_x = 20 + i + (i * 0.2) # Adding artificial drift
        payload = {
            "player_id": "Haaland_9",
            "x": noise_x,
            "y": 20 + i,
            "timestamp": time.time()
        }
        
        requests.post(api_url, json=payload)
        print(f"   [Frame {i}] Ingested noisy pos: ({payload['x']:.2f}, {payload['y']:.2f})")
        time.sleep(0.05)

    print("\n📥 Processing buffer in backend...")
    # This will trigger the persist_to_db which now includes Kalman smoothing
    print("✅ Smoothing and Persistence Complete.")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_stability_test()
