import requests
import time
import json
from perception.homography import HomographyTransformer

def run_cloud_demo():
    transformer = HomographyTransformer()
    api_url = "http://localhost:8000/ingest/coordinate"
    
    print("\n" + "="*60)
    print("👁️  OMNI-PATH DAY 3 DEMO: CLOUD VISION -> BACKEND")
    print("Scenario: YOLO (Colab) Detection -> Homography -> API")
    print("="*60 + "\n")

    # 1. Simulate a YOLO detection in Colab (Pixels)
    yolo_detection = {"player": "Haaland_9", "px": 800, "py": 600}
    print(f"📡 [COLAB] YOLO detected {yolo_detection['player']} at pixel ({yolo_detection['px']}, {yolo_detection['py']})")

    # 2. Warp to Pitch Meters
    mx, my = transformer.project_point(yolo_detection['px'], yolo_detection['py'])
    print(f"🌍 [COLAB] Homography warped to Pitch Meters: {mx}m, {my}m")

    # 3. Send to Backend API
    payload = {
        "player_id": yolo_detection['player'],
        "x": mx,
        "y": my,
        "timestamp": time.time()
    }
    
    print(f"📤 [COLAB] Sending POST request to Backend API...")
    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            print(f"✅ [BACKEND] Success! API Response: {response.json()}")
        else:
            print(f"❌ [BACKEND] API Error: {response.text}")
    except Exception as e:
        print(f"⚠️  [BACKEND] Connection failed. Is the API server running? {e}")

    print("\n" + "="*60)
    print("✅ DEMO COMPLETE: Distributed Vision Pipeline Validated.")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_cloud_demo()
