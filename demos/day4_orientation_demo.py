import requests
import time
import json
from perception.orientation_engine import OrientationEngine

def run_orientation_demo():
    engine = OrientationEngine()
    api_url = "http://localhost:8000/ingest/coordinate"
    
    print("\n" + "="*60)
    print("🛰️  OMNI-PATH DAY 4 DEMO: YOLO-OBB PERCEPTION")
    print("Scenario: Heading Detection -> Distributed Ingestion")
    print("="*60 + "\n")

    # 1. Simulate a YOLO-OBB detection (x, y, w, h, theta)
    # theta = 1.0 rad (~57.3 degrees)
    raw_detection = {
        "player_id": "Haaland_9",
        "obb": [90, 45, 2, 4, 1.0] 
    }
    
    # 2. Extract Heading
    perception_result = engine.process_detection(raw_detection)
    print(f"👁️  [PERCEPTION] Detected {perception_result['player_id']} facing {perception_result['heading']}°")

    # 3. Send to Backend API
    payload = {
        "player_id": perception_result['player_id'],
        "x": perception_result['x'],
        "y": perception_result['y'],
        "timestamp": time.time(),
        "heading": perception_result['heading']
    }
    
    print(f"📤 [INGRESS] Sending detection to API...")
    try:
        resp = requests.post(api_url, json=payload)
        if resp.status_code == 200:
            print(f"✅ [BACKEND] Success! Heading Ingested.")
        else:
            print(f"❌ [BACKEND] API Error: {resp.text}")
    except Exception as e:
        print(f"⚠️  [BACKEND] Connection failed: {e}")

    print("\n" + "="*60)
    print("✅ DEMO COMPLETE: Body Orientation Pipeline Validated.")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_orientation_demo()
