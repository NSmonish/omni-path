import numpy as np
import cv2
from perception.homography import HomographyTransformer

def demo_homography_projection():
    transformer = HomographyTransformer()
    
    print("\n" + "="*60)
    print("👁️  OMNI-PATH CV DEMO: BIRD'S EYE PROJECTION")
    print("Scenario: Projecting Broadcast Pixels to 2D Pitch Meters")
    print("="*60 + "\n")

    # 1. Simulate detections in a 1920x1080 broadcast frame
    # Format: [name, x_pixel, y_pixel]
    detections = [
        ["Haaland (9)", 600, 650], 
        ["Foden (47)", 850, 680],
        ["Chelsea_CB", 1000, 720],
        ["Penalty Spot", 420, 610]
    ]

    print(f"{'Player/Point':<15} | {'TV Pixels':<15} | {'Pitch Meters':<15}")
    print("-" * 55)

    for name, px, py in detections:
        # Warp pixel to meters
        mx, my = transformer.project_point(px, py)
        print(f"{name:<15} | ({px}, {py}) | {mx}m, {my}m")

    print("\n✅ PROJECTED DATA READY FOR TDA & PITCH CONTROL.")
    print("="*60 + "\n")

if __name__ == "__main__":
    demo_homography_projection()
