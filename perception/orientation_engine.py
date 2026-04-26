import numpy as np
import logging

logger = logging.getLogger("OrientationEngine")

class OrientationEngine:
    """
    Processes YOLOv11-OBB (Oriented Bounding Boxes) to extract player heading.
    OBB typically returns [x, y, w, h, theta] where theta is the box rotation.
    """
    def __init__(self):
        pass

    def extract_heading(self, theta_rad):
        """
        Normalizes YOLO OBB angle (radians) to standard 0-360 degrees.
        """
        # Convert to degrees
        degrees = np.degrees(theta_rad)
        
        # Normalize to [0, 360)
        heading = degrees % 360
        return round(float(heading), 2)

    def process_detection(self, detection):
        """
        Processes a raw OBB detection.
        Detection format: {"player_id": str, "obb": [x, y, w, h, theta]}
        """
        theta = detection["obb"][4]
        heading = self.extract_heading(theta)
        
        return {
            "player_id": detection["player_id"],
            "x": detection["obb"][0],
            "y": detection["obb"][1],
            "heading": heading
        }

if __name__ == "__main__":
    engine = OrientationEngine()
    
    # Simulate a Haaland detection sprinting towards goal
    # theta = 0.5 radians (~28.6 degrees)
    detection = {
        "player_id": "Haaland_9",
        "obb": [100, 40, 2, 5, 0.5] 
    }
    
    result = engine.process_detection(detection)
    print(f"👁️  YOLO-OBB Perception:")
    print(f"   - Player: {result['player_id']}")
    print(f"   - Position: ({result['x']}, {result['y']})")
    print(f"   - Extracted Heading: {result['heading']}°")
    
    if 0 <= result['heading'] <= 90:
        print("   ✅ Player is facing the Attacking Third.")
